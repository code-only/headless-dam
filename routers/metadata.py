from typing import List, Optional, Dict
from uuid import UUID
from fastapi import APIRouter, Path, status, Body, Query, HTTPException, Depends
from pydantic import BaseModel, HttpUrl, constr, Field
from sqlalchemy.orm import Session

from db import get_db
from models import Webhook
from dependencies.auth import get_current_user, TokenPayload

router = APIRouter()

# --- Pydantic Models ---


class WebhookBase(BaseModel):
    url: HttpUrl
    events: List[constr(min_length=1)]
    secret: Optional[constr(min_length=8, max_length=128)] = None
    is_active: bool = True
    description: Optional[str] = None
    headers: Optional[Dict[str, str]] = Field(
        default_factory=dict, description="Custom HTTP headers"
    )


class WebhookCreate(WebhookBase):
    pass


class WebhookUpdate(BaseModel):
    url: Optional[HttpUrl] = None
    events: Optional[List[constr(min_length=1)]] = None
    secret: Optional[constr(min_length=8, max_length=128)] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None
    headers: Optional[Dict[str, str]] = None


class WebhookResponse(WebhookBase):
    id: UUID


class WebhookListResponse(BaseModel):
    items: List[WebhookResponse]
    total: int


class MessageResponse(BaseModel):
    message: str


# --- Endpoints ---


@router.get("/", response_model=WebhookListResponse)
def list_webhooks(
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    event: Optional[str] = Query(None, description="Filter by event type"),
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    """
    List all webhooks for the current tenant.
    Supports filtering by active status and event type.
    """
    query = db.query(Webhook).filter(Webhook.tenant_id == current_user.tenant_id)
    if is_active is not None:
        query = query.filter(Webhook.is_active == is_active)
    if event:
        query = query.filter(Webhook.events.contains([event]))
    items = query.all()
    return WebhookListResponse(
        items=[
            WebhookResponse(
                id=w.id,
                url=w.url,
                events=w.events,
                secret=w.secret,
                is_active=w.is_active,
                description=w.description,
                headers=w.headers,
            )
            for w in items
        ],
        total=len(items),
    )


@router.post("/", response_model=WebhookResponse, status_code=status.HTTP_201_CREATED)
def create_webhook(
    webhook: WebhookCreate,
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    """
    Create a new webhook for the current tenant.
    - `webhook`: Webhook details to create.
    """
    db_webhook = Webhook(
        url=webhook.url,
        events=webhook.events,
        secret=webhook.secret,
        is_active=webhook.is_active,
        description=webhook.description,
        headers=webhook.headers,
        tenant_id=current_user.tenant_id,
    )
    db.add(db_webhook)
    db.commit()
    db.refresh(db_webhook)
    return WebhookResponse(
        id=db_webhook.id,
        url=db_webhook.url,
        events=db_webhook.events,
        secret=db_webhook.secret,
        is_active=db_webhook.is_active,
        description=db_webhook.description,
        headers=db_webhook.headers,
    )


@router.patch("/{id}", response_model=WebhookResponse)
def update_webhook(
    id: UUID = Path(..., description="Webhook ID"),
    webhook: WebhookUpdate = Body(...),
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    db_webhook = (
        db.query(Webhook)
        .filter(Webhook.id == str(id), Webhook.tenant_id == current_user.tenant_id)
        .first()
    )
    if not db_webhook:
        raise HTTPException(404, "Webhook not found")
    for field, value in webhook.dict(exclude_unset=True).items():
        setattr(db_webhook, field, value)
    db.commit()
    db.refresh(db_webhook)
    return WebhookResponse(
        id=db_webhook.id,
        url=db_webhook.url,
        events=db_webhook.events,
        secret=db_webhook.secret,
        is_active=db_webhook.is_active,
        description=db_webhook.description,
        headers=db_webhook.headers,
    )


@router.delete("/{id}", response_model=MessageResponse)
def delete_webhook(
    id: UUID = Path(..., description="Webhook ID"),
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    """
    Delete a webhook by ID for the current tenant.
    - `id`: Webhook ID to delete.
    """
    db_webhook = (
        db.query(Webhook)
        .filter(Webhook.id == str(id), Webhook.tenant_id == current_user.tenant_id)
        .first()
    )
    if not db_webhook:
        raise HTTPException(404, "Webhook not found")
    db.delete(db_webhook)
    db.commit()
    return MessageResponse(message="Webhook deleted successfully")

