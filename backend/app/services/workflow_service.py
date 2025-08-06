from pymongo import MongoClient
from core.config import settings
from automation_service import AutomationService
from constants import MONGODB_WORKFLOW_COLLECTION_NAME, MONGODB_AUTOMATION_LOGS_COLLECTION_NAME

class WorkflowService:
    def __init__(self, automation_service: AutomationService):
        self.automation_service = automation_service
        self.mongo_client = MongoClient(settings.MONGODB_URL)
        self.db = self.mongo_client[MONGODB_WORKFLOW_COLLECTION_NAME]
        self.logs_collection = self.db[MONGODB_AUTOMATION_LOGS_COLLECTION_NAME]

    def execute_and_log_workflow(self, workflow_definition: dict):
        steps = workflow_definition.get("steps", [])
        self.automation_service.execute_steps(steps)
        
        self.logs_collection.insert_one({
            "workflow_name": workflow_definition.get("workflow_name", "Unnamed Workflow"),
            "steps": steps,
            "status": "completed"
        })
