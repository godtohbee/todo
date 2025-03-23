from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attribute = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
