from fastapi import APIRouter, Path, status, Body, Query
from pydantic import BaseModel, constr, Field
from typing import List, Optional
from uuid import UUID

router = APIRouter()

# --- Request/Response Models ---

class TagCreate(BaseModel):
    name: constr(min_length=1, max_length=64)
    description: Optional[str] = None

class TagResponse(TagCreate):
    id: UUID

class TagListResponse(BaseModel):
    items: List[TagResponse]
    total: int

class AssetTagsUpdate(BaseModel):
    tags: List[constr(min_length=1, max_length=64)] = Field(..., description="List of tag names to set for the asset")

class MessageResponse(BaseModel):
    message: str

# --- Endpoints ---

@router.get("/", response_model=TagListResponse)
async def list_tags(
    q: Optional[str] = Query(None, description="Search tags by name"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size")
):
    """
    List all tags, with optional search and pagination.
    """
    # TODO: Return tags, optionally filtered by search query
    pass

@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag: TagCreate
):
    """
    Create a new tag.
    """
    # TODO: Validate and create tag, return TagResponse
    pass

@router.patch("/assets/{id}/tags", response_model=MessageResponse)
async def update_asset_tags(
    id: UUID = Path(..., description="Asset ID"),
    update: AssetTagsUpdate = Body(...)
):
    """
    Add or remove tags for an asset (replace with provided list).
    """
    # TODO: Update asset's tags, return confirmation message
    pass

