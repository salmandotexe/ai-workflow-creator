from fastapi import FastAPI
from app.api.v1 import workflow
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

app.include_router(workflow.router, prefix="/api/v1")
Instrumentator().instrument(app).expose(app)
