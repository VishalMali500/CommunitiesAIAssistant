from pydantic_settings import BaseSettings
from pydantic import Field, BaseModel


class RoleSettings(BaseModel):
    roles_db : dict = Field(default_factory=lambda: {
    "vishal": "user",
    "vaibhav": "user",
    "shiva": "user"
})
    
def getrole()-> RoleSettings:
    return RoleSettings()
