from typing import List
from uuid import UUID
from fastapi import APIRouter, Path, Body
from pydantic import BaseModel, constr, Field

router = APIRouter()

# --- Request/Response Models ---


class Permission(BaseModel):
    subject: constr(min_length=1)  # user or group identifier
    level: constr(regex="^(read|write|admin)$")
    type: constr(regex="^(user|group)$")


class AssetPermissionsUpdate(BaseModel):
    permissions: List[Permission] = Field(
        ..., description="List of permissions to set for the asset"
    )


class PermissionsResponse(BaseModel):
    permissions: List[Permission]


class MessageResponse(BaseModel):
    message: str


# --- Endpoints ---


@router.get("/", response_model=PermissionsResponse)
async def list_permissions():
    """
    List all available permissions/roles.
    """
    # TODO: Return all possible permissions/roles
    pass


@router.patch("/assets/{id}/permissions", response_model=MessageResponse)
async def update_asset_permissions(
    id: UUID = Path(..., description="Asset ID"),
    update: AssetPermissionsUpdate = Body(...),
):
    """
    Set or update asset-level permissions.
    """
    # TODO: Update asset permissions, return confirmation message
    pass

