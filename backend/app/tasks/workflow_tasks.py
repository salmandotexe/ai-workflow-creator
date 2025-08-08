from celery import Celery
from app.services.automation_service import AutomationService
from app.services.workflow_service import WorkflowService
from app.services.storage_service import StorageService
from typing import Optional
from app.constants import CELERY_WORKFLOW_TASKS_NAME
from app.core.config import get_settings

app_settings = get_settings()

celery_app = Celery(
    CELERY_WORKFLOW_TASKS_NAME,
    broker=app_settings.RABBITMQ_URL,
    backend=f"{app_settings.MONGODB_URL}{app_settings.CELERY_BACKEND_DB}"
)

@celery_app.task
def execute_dynamic_workflow(workflow_definition: dict):
    """
    Celery task to execute a workflow. It is self-contained.
    It instantiates its own services, ensuring no non-serializable
    objects are passed as arguments.
    """
    # The task now creates its own settings and service instances.
    task_settings = get_settings()
    workflow_service = WorkflowService(settings=task_settings)
    
    # Now call the service method.
    return workflow_service.execute_and_log_workflow(workflow_definition)