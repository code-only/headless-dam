from fastapi import APIRouter, Path, status
from pydantic import BaseModel
from uuid import UUID

router = APIRouter()

# --- Response Models ---

class MessageResponse(BaseModel):
    message: str

# --- Endpoints ---

@router.delete("/{id}", response_model=MessageResponse)
async def delete_asset(
    id: UUID = Path(..., description="Asset ID")
):
    """
    Delete (soft or hard) an asset.
    """
    # TODO: Implement soft/hard delete logic, return confirmation message
    pass

@router.post("/{id}/restore", response_model=MessageResponse)
async def restore_asset(
    id: UUID = Path(..., description="Asset ID")
):
    """
    Restore a deleted asset.
    """
    # TODO: Restore asset, return confirmation message
    pass

@router.post("/{id}/archive", response_model=MessageResponse)
async def archive_asset(
    id: UUID = Path(..., description="Asset ID")
):
    """
    Archive an asset.
    """
    # TODO: Archive asset, return confirmation message
    pass

@router.post("/{id}/unarchive", response_model=MessageResponse)
async def unarchive_asset(
    id: UUID = Path(..., description="Asset ID")
):
    """
    Unarchive an asset.
    """
    # TODO: Unarchive asset, return confirmation message
    pass

