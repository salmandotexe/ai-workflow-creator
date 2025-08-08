from pydantic import BaseModel
from typing import List

class UserInstruction(BaseModel):
    instruction: str = None

class WorkflowDefinition(BaseModel):
    steps: List[dict] = None