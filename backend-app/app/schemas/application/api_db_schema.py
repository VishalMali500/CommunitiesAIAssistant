from pydantic import BaseModel, field_validator
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Integer, String, Boolean, Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
import re
from typing import Optional

Base = declarative_base()

class CreateUser(BaseModel):
    id : str
    password : str
    name : str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one digit")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")

        return value
    


class LoginUser(BaseModel):
    id : str 
    password : str


class DbUser(Base):
    __tablename__ = "UserDataTable"
    name = Column(String, nullable=False)
    id = Column(String, nullable=False, primary_key=True, index=True)
    hashed_password = Column(String, nullable= False)
    role = Column(String, nullable=False)
    chatthreads = relationship("chatThreads", back_populates= "user", cascade="all, delete-orphan")

class chatThreads(Base):
    __tablename__ = "ChatThreadsTable"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,index=True)
    user_id = Column(String, ForeignKey("UserDataTable.id"),nullable=False)
    title = Column(String, nullable= False)
    created_at = Column(DateTime, nullable= False)
    updated_at = Column(DateTime, nullable= False)
    user = relationship("DbUser", back_populates="chatthreads" )
    chatlists = relationship("chatLists", back_populates="chatthread", cascade="all, delete-orphan")

class chatLists(Base):
    __tablename__ = "ChatLists"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,index=True)
    chatthread_id = Column(UUID(as_uuid=True), ForeignKey("ChatThreadsTable.id"), nullable=False)
    content = Column(String, nullable=False)
    role = Column(String, nullable= False)
    created_at = Column(DateTime, nullable= False)
    chatthread = relationship("chatThreads", back_populates="chatlists")


class newChat(BaseModel):
    threadid : Optional[uuid.UUID] = None
    user : str
    query : str 





