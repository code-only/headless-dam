from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Dict, Any

router = APIRouter()

# --- Response Models ---

class HealthResponse(BaseModel):
    status: str = Field(..., example="ok")
    details: Dict[str, Any] = Field(default_factory=dict)

class ConfigResponse(BaseModel):
    version: str
    environment: str
    features: Dict[str, bool]

# --- Endpoints ---

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    """
    # Example health checks for services (DB, storage, etc.)
    # In real code, replace with actual checks.
    details = {
        "database": "ok",
        "storage": "ok"
    }
    return HealthResponse(status="ok", details=details)

@router.get("/config", response_model=ConfigResponse)
async def get_config():
    """
    Get system configuration.
    """
    # TODO: Return system configuration and enabled features
    pass

