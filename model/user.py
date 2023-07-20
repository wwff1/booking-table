from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = ''
    login: str = Field(default='', include=True)
    email: str = Field(include=True)
    name: str = Field(default='', include=True)
    phone: str = Field(default='', include=True)
    password: Optional[str] = Field(include=False)
