from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, constr
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

from config import settings

from db import get_db
from models import User

router = APIRouter()


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Request/Response Models ---

class LoginRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=128)

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds

class RefreshRequest(BaseModel):
    refresh_token: str

class MessageResponse(BaseModel):
    message: str

# --- Endpoints ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and obtain access/refresh tokens.
    """
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")
    access_token = create_access_token({
        "sub": str(user.id),
        "tenant_id": user.tenant_id,
        "email": user.email,
        "roles": user.roles
    })
    refresh_token = create_refresh_token({
        "sub": str(user.id),
        "tenant_id": user.tenant_id,
        "email": user.email,
        "roles": user.roles
    })
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def refresh(payload: RefreshRequest):
    try:
        payload_data = jwt.decode(payload.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        # Optionally, check for token revocation/blacklist here
        user_id = payload_data.get("sub")
        tenant_id = payload_data.get("tenant_id")
        email = payload_data.get("email")
        roles = payload_data.get("roles", [])
        if not user_id or not tenant_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token.")
        # Generate new tokens
        access_token = create_access_token({
            "sub": user_id,
            "tenant_id": tenant_id,
            "email": email,
            "roles": roles
        })
        refresh_token = create_refresh_token({
            "sub": user_id,
            "tenant_id": tenant_id,
            "email": email,
            "roles": roles
        })
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token.")

