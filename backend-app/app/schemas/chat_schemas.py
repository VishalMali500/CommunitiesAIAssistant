from pydantic import BaseModel
from typing import Optional
from uuid import UUID
class UserQuery(BaseModel):
    chatid: UUID
    query : str 