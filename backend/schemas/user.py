# backend/app/schemas/user.py
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str
    email: str
    password: str = Field(..., min_length=6, max_length=72)
    is_provider: bool = False

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_provider: bool

    class Config:
        orm_mode = True
