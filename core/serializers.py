from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserBaseSerializer(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreateSerializer(UserBaseSerializer):
    password: str

class UserResponseSerializer(UserBaseSerializer):
    id: int
    is_active: bool
    is_staff: bool
    date_joined: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CategorySerializer(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    slug: str
    
    class Config:
        from_attributes = True

class PostBaseSerializer(BaseModel):
    title: str
    content: str
    category_id: Optional[int] = None

class PostCreateSerializer(PostBaseSerializer):
    author_id: int

class PostResponseSerializer(PostBaseSerializer):
    id: int
    slug: str
    author_id: int
    is_published: bool
    created_at: datetime
    published_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True