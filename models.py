# models.py
from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    DateTime,
    JSON,
    Text,
)
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.sql import func
from uuid import uuid4
from db import Base


def generate_uuid():
    return str(uuid4())


class User(Base):
    __tablename__ = "users"
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), index=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(128))
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    roles = Column(JSON, default=[])
    created_at = Column(DateTime, server_default=func.now())


class Asset(Base):
    __tablename__ = "assets"
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), index=True, nullable=False)
    filename = Column(String(255), nullable=False)
    url = Column(Text, nullable=False)
    mimetype = Column(String(128), nullable=False)
    size = Column(Integer, nullable=False)
    metainfo = Column(JSON, default={})
    version = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Tag(Base):
    __tablename__ = "tags"
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), index=True, nullable=False)
    name = Column(String(64), nullable=False)
    description = Column(String(255))


class Webhook(Base):
    __tablename__ = "webhooks"
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), index=True, nullable=False)
    url = Column(Text, nullable=False)
    events = Column(JSON, default=[])
    secret = Column(String(128))
    is_active = Column(Boolean, default=True)
    description = Column(String(255))
    headers = Column(JSON, default={})

