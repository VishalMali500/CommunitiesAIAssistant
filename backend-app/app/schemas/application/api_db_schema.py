from pydantic import BaseModel, field_validator
from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, String, Boolean, Column

import re

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
    
class DbUser(Base):
    __tablename__ = "UserDataTable"
    name = Column(String, nullable=False)
    id = Column(String, nullable=False, primary_key=True, index=True)
    hashed_password = Column(String, nullable= False)
    role = Column(String, nullable=False)
