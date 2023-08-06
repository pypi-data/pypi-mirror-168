from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    phone: Optional[str]
    password: str
    role: str = "user"
    permission: list = []
