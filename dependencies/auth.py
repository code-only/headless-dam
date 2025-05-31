from fastapi import HTTPException, status, Request
from pydantic import BaseModel
from typing import Optional
from jose import jwt, JWTError

from config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM


class TokenPayload(BaseModel):
    sub: str
    tenant_id: str
    exp: int
    email: Optional[str] = None
    roles: Optional[list] = []


def get_current_user(request: Request) -> TokenPayload:
    """
    Extracts the current user from the request using the JWT token in the Authorization header.
    Raises HTTPException if the token is missing or invalid.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token."
        )
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload(**payload)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

