from celery import Celery
from app.core.config import settings
from app.services.automation_service import AutomationService
from app.services.workflow_service import WorkflowService
from app.constants import CELERY_WORKFLOW_TASKS_NAME

celery_app = Celery(
    CELERY_WORKFLOW_TASKS_NAME,
    broker=settings.RABBITMQ_URL,
    backend=f"{settings.MONGODB_URL}{settings.CELERY_BACKEND_DB}"
)

automation_service = AutomationService()
workflow_service = WorkflowService(automation_service)

@celery_app.task
def execute_dynamic_workflow(workflow_definition: dict):
    workflow_service.execute_and_log_workflow(workflow_definition)
