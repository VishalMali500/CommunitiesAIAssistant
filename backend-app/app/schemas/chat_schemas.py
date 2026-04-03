from pydantic import BaseModel
from typing import Optional

class UserQuery(BaseModel):
    chatid: Optional[str] = None
    query : str 