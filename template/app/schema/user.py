from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserLogin(BaseModel):
    email: EmailStr
    password: str
class UserCreate(UserLogin):
    full_name: Optional[str]
    organization_id: Optional[str]


class UserRead(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str]
    roles: List[Role]





class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
