from fastapi import FastAPI
from api.v1 import workflow

app = FastAPI()

app.include_router(workflow.router, prefix="/api/v1")
