# create_first_user.py
from db import SessionLocal
from models import User
from passlib.context import CryptContext
from uuid import uuid4

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_first_user():
    """
    Create the first user with admin privileges.
    This function should be run only once to set up the initial admin user.
    """
    db = SessionLocal()
    user = User(
        id=str(uuid4()),
        tenant_id="ten1",
        email="admin@example.com",
        full_name="Admin User",
        password_hash=get_password_hash("adminpassword"),
        is_active=True,
        roles=["admin"],
    )
    db.add(user)
    db.commit()
    db.close()
    print("First user created!")


if __name__ == "__main__":
    create_first_user()

