from pymongo import MongoClient
from app.core.config import Settings
from app.services.automation_service import AutomationService
from typing import Optional, List
import uuid
from app.constants import MONGODB_WORKFLOW_COLLECTION_NAME, MONGODB_AUTOMATION_LOGS_COLLECTION_NAME

class WorkflowService:
    """
    Manages the execution of workflows and logs the results to MongoDB.
    """
    def __init__(self, settings: Settings):
        self.settings = settings
        # The service creates its own dependencies.
        self.automation_service = AutomationService(settings=self.settings)
        self.mongo_client = MongoClient(settings.MONGODB_URL)
        self.db = self.mongo_client[MONGODB_WORKFLOW_COLLECTION_NAME]
        self.logs_collection = self.db[MONGODB_AUTOMATION_LOGS_COLLECTION_NAME]

    def execute_and_log_workflow(self, workflow_definition: dict) -> List[str]:
        """
        Executes workflow steps via the AutomationService and logs the outcome.
        """
        steps = workflow_definition.get("steps", [])
        # The dependency (AutomationService) is internal to the class.
        result_file_names = self.automation_service.execute_steps(steps)
        
        self.logs_collection.insert_one({
            "workflow_name": workflow_definition.get("workflow_name", "Unnamed Workflow"),
            "steps": steps,
            "status": "completed",
            "output_files": result_file_names,
            "timestamp": uuid.uuid4().hex # Example of adding a timestamp
        })
        return result_file_names