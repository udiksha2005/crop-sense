from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Uuid
import uuid
from datetime import datetime
from .connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    solution = Column(String)

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=True)
    filename = Column(String)
    image_path = Column(String, nullable=True)
    crop_name = Column(String)
    disease_name = Column(String)
    confidence = Column(Float)
    severity = Column(String, nullable=True)
    model_version = Column(String, default="1.0.0")
    processing_time = Column(Float, nullable=True)
    status = Column(String, default="completed")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
