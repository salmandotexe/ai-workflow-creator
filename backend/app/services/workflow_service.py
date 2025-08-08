from pymongo import MongoClient
from app.core.config import settings
from app.services.automation_service import AutomationService
from app.services.storage_service import StorageService
from typing import Optional
from app.constants import MONGODB_WORKFLOW_COLLECTION_NAME, MONGODB_AUTOMATION_LOGS_COLLECTION_NAME

class WorkflowService:
    def __init__(self, automation_service: AutomationService):
        self.automation_service = automation_service
        self.mongo_client = MongoClient(settings.MONGODB_URL)
        self.db = self.mongo_client[MONGODB_WORKFLOW_COLLECTION_NAME]
        self.logs_collection = self.db[MONGODB_AUTOMATION_LOGS_COLLECTION_NAME]

    def execute_and_log_workflow(self, workflow_definition: dict, storage_service: Optional[StorageService] = None):
        steps = workflow_definition.get("steps", [])
        result = self.automation_service.execute_steps(steps, storage_service)
        
        self.logs_collection.insert_one({
            "workflow_name": workflow_definition.get("workflow_name", "Unnamed Workflow"),
            "steps": steps,
            "status": "completed"
        })
        return result
