import uuid
from pathlib import Path
from fastapi import Depends
from app.core.config import get_settings, Settings

class StorageService: # Later we can refactor this to use S3 by making it a subclass
    def __init__(self, settings: Settings = Depends(get_settings)):
        self.storage_path = settings.STORAGE_DIR
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def save_file(self, content: bytes, extension=".png") -> str:
        filename = f"{uuid.uuid4().hex}{extension}"
        filepath = self.storage_path / filename
        with open(filepath, "wb") as f:
            f.write(content)
        return filename

    def get_file_path(self, filename: str) -> Path:
        path = self.storage_path / filename
        if not path.exists():
            raise FileNotFoundError(f"{filename} not found")
        return path

def get_storage_service() -> StorageService:
    """
    Factory function to get a pre-configured StorageService instance.
    This function is used to inject the service into FastAPI endpoints.
    """
    return StorageService()