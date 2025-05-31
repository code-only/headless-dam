from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Path, Query, status, HTTPException, Depends, Body
from pydantic import BaseModel, EmailStr, constr, Field
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from db import get_db
from models import User
from dependencies.auth import get_current_user, TokenPayload

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Pydantic Models ---


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[constr(min_length=1, max_length=128)] = None
    is_active: bool = True
    roles: List[str] = Field(default_factory=list, description="List of user roles")


class UserCreate(UserBase):
    password: constr(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    full_name: Optional[constr(min_length=1, max_length=128)] = None
    password: Optional[constr(min_length=8, max_length=128)] = None
    is_active: Optional[bool] = None
    roles: Optional[List[str]] = None


class UserResponse(UserBase):
    id: UUID


class UserListResponse(BaseModel):
    items: List[UserResponse]
    total: int
    page: int
    size: int


class MessageResponse(BaseModel):
    message: str


# --- Helper Functions ---


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# --- Endpoints ---


@router.get("/", response_model=UserListResponse)
def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    q: Optional[str] = Query(None, description="Search by email or name"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    role: Optional[str] = Query(None, description="Filter by role"),
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    """
    List users in the current tenant with optional filters and pagination.
    - `page`: Page number for pagination (default 1).
    - `size`: Number of users per page (default 20, max 100).
    - `q`: Search query to filter by email or full name.
    - `is_active`: Filter by active status (True/False).
    - `role`: Filter by user role.
    """
    query = db.query(User).filter(User.tenant_id == current_user.tenant_id)
    if q:
        query = query.filter(
            (User.email.like(f"%{q}%")) | (User.full_name.like(f"%{q}%"))
        )
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    if role:
        query = query.filter(User.roles.contains([role]))
    total = query.count()
    users = query.offset((page - 1) * size).limit(size).all()
    return UserListResponse(
        items=[
            UserResponse(
                id=u.id,
                email=u.email,
                full_name=u.full_name,
                is_active=u.is_active,
                roles=u.roles,
            )
            for u in users
        ],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{id}", response_model=UserResponse)
def get_user(
    id: UUID = Path(..., description="User ID"),
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    """
    Get user details by ID in the current tenant.
    - `id`: User ID to retrieve.
    """
    user = (
        db.query(User)
        .filter(User.id == str(id), User.tenant_id == current_user.tenant_id)
        .first()
    )
    if not user:
        raise HTTPException(404, "User not found")
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        roles=user.roles,
    )


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    """
    Create a new user in the current tenant.
    - `user`: User details to create.
    """
    # Check for existing email in this tenant
    existing = (
        db.query(User)
        .filter(User.email == user.email, User.tenant_id == current_user.tenant_id)
        .first()
    )
    if existing:
        raise HTTPException(400, "Email already registered.")
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        roles=user.roles,
        password_hash=get_password_hash(user.password),
        tenant_id=current_user.tenant_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponse(
        id=db_user.id,
        email=db_user.email,
        full_name=db_user.full_name,
        is_active=db_user.is_active,
        roles=db_user.roles,
    )


@router.patch("/{id}", response_model=UserResponse)
def update_user(
    id: UUID = Path(..., description="User ID"),
    user: UserUpdate = Body(...),
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    """
    Update an existing user in the current tenant.
    - `id`: User ID to update.
    - `user`: User details to update (can include full_name, password, is_active, roles).
    """
    db_user = (
        db.query(User)
        .filter(User.id == str(id), User.tenant_id == current_user.tenant_id)
        .first()
    )
    if not db_user:
        raise HTTPException(404, "User not found")
    if user.full_name is not None:
        db_user.full_name = user.full_name
    if user.is_active is not None:
        db_user.is_active = user.is_active
    if user.roles is not None:
        db_user.roles = user.roles
    if user.password is not None:
        db_user.password_hash = get_password_hash(user.password)
    db.commit()
    db.refresh(db_user)
    return UserResponse(
        id=db_user.id,
        email=db_user.email,
        full_name=db_user.full_name,
        is_active=db_user.is_active,
        roles=db_user.roles,
    )


@router.delete("/{id}", response_model=MessageResponse)
def delete_user(
    id: UUID = Path(..., description="User ID"),
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    """
    Delete a user by ID in the current tenant.
    - `id`: User ID to delete.
    """
    db_user = (
        db.query(User)
        .filter(User.id == str(id), User.tenant_id == current_user.tenant_id)
        .first()
    )
    if not db_user:
        raise HTTPException(404, "User not found.")
    db.delete(db_user)
    db.commit()
    return MessageResponse(message="User deleted successfully.")

