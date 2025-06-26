from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .models import User, Post, Category
from .serializers import (
    UserCreateSerializer, UserResponseSerializer,
    PostCreateSerializer, PostResponseSerializer,
    CategorySerializer
)

router = APIRouter()



# User Views
@router.post("/users/", response_model=UserResponseSerializer)
async def create_user_view(user: UserCreateSerializer, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    db_user = User(**user.dict(exclude={'password'}))
    # In real app, hash the password here
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user







@router.get("/users/", response_model=List[UserResponseSerializer])
async def list_users_view(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List all users with pagination and search"""
    query = db.query(User)
    
    if search:
        query = query.filter(
            (User.username.contains(search)) | 
            (User.email.contains(search))
        )
    
    users = query.offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=UserResponseSerializer)
async def get_user_view(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user




# Post Views
@router.post("/posts/", response_model=PostResponseSerializer)
async def create_post_view(post: PostCreateSerializer, db: Session = Depends(get_db)):
    """Create a new post"""
    # Generate slug from title
    slug = post.title.lower().replace(" ", "-").replace(".", "")
    
    db_post = Post(**post.dict(), slug=slug)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/posts/", response_model=List[PostResponseSerializer])
async def list_posts_view(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    published_only: bool = Query(False),
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List posts with filtering options"""
    query = db.query(Post)
    
    if published_only:
        query = query.filter(Post.is_published == True)
    
    if category_id:
        query = query.filter(Post.category_id == category_id)
    
    posts = query.offset(skip).limit(limit).all()
    return posts






# core/__init__.py
"""
Core module initialization
"""

# core/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/admin", tags=["admin"])

# Admin routes for managing the application
@router.get("/dashboard")
async def admin_dashboard():
    return {
        "message": "Admin Dashboard",
        "modules": ["users", "posts", "settings"],
        "status": "active"
    }

@router.get("/users/stats")
async def user_stats():
    return {
        "total_users": 150,
        "active_users": 120,
        "new_users_today": 5
    }

# core/apps.py
"""
App configuration for core module
"""
class CoreConfig:
    name = 'core'
    verbose_name = 'Core Application'
    
    def __init__(self):
        self.routes = [
            "/api/users/",
            "/api/posts/",
            "/admin/"
        ]

# core/models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(BaseModel):
    __tablename__ = "core_users"
    
    username = Column(String(150), unique=True, index=True, nullable=False)
    email = Column(String(254), unique=True, index=True, nullable=False)
    first_name = Column(String(30))
    last_name = Column(String(150))
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    date_joined = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

class Category(BaseModel):
    __tablename__ = "core_categories"
    
    name = Column(String(100), nullable=False)
    description = Column(Text)
    slug = Column(String(100), unique=True, index=True)

class Post(BaseModel):
    __tablename__ = "core_posts"
    
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, index=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("core_users.id"))
    category_id = Column(Integer, ForeignKey("core_categories.id"))
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime)
    
    # Relationships would be defined here in SQLAlchemy
    # author = relationship("User", back_populates="posts")
    # category = relationship("Category", back_populates="posts")

# core/serializers.py
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

# core/tests.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_create_user():
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User"
    }
    response = client.post("/api/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_get_users():
    response = client.get("/api/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# core/urls.py
from fastapi import APIRouter
from . import views

router = APIRouter()

# URL patterns equivalent
urlpatterns = [
    {"path": "/api/users/", "methods": ["GET", "POST"], "handler": "users"},
    {"path": "/api/users/{user_id}", "methods": ["GET", "PUT", "DELETE"], "handler": "user_detail"},
    {"path": "/api/posts/", "methods": ["GET", "POST"], "handler": "posts"},
    {"path": "/api/posts/{post_id}", "methods": ["GET", "PUT", "DELETE"], "handler": "post_detail"},
    {"path": "/api/categories/", "methods": ["GET", "POST"], "handler": "categories"},
    {"path": "/admin/", "methods": ["GET"], "handler": "admin_panel"},
]

# Route registration function
def include_router(app):
    """Include all core routes in the main FastAPI app"""
    from .views import router as core_router
    app.include_router(core_router, prefix="/core")

# core/views.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .models import User, Post, Category
from .serializers import (
    UserCreateSerializer, UserResponseSerializer,
    PostCreateSerializer, PostResponseSerializer,
    CategorySerializer
)

router = APIRouter()

# User Views
@router.post("/users/", response_model=UserResponseSerializer)
async def create_user_view(user: UserCreateSerializer, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    db_user = User(**user.dict(exclude={'password'}))
    # In real app, hash the password here
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/", response_model=List[UserResponseSerializer])
async def list_users_view(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List all users with pagination and search"""
    query = db.query(User)
    
    if search:
        query = query.filter(
            (User.username.contains(search)) | 
            (User.email.contains(search))
        )
    
    users = query.offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=UserResponseSerializer)
async def get_user_view(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Post Views
@router.post("/posts/", response_model=PostResponseSerializer)
async def create_post_view(post: PostCreateSerializer, db: Session = Depends(get_db)):
    """Create a new post"""
    # Generate slug from title
    slug = post.title.lower().replace(" ", "-").replace(".", "")
    
    db_post = Post(**post.dict(), slug=slug)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/posts/", response_model=List[PostResponseSerializer])
async def list_posts_view(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    published_only: bool = Query(False),
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List posts with filtering options"""
    query = db.query(Post)
    
    if published_only:
        query = query.filter(Post.is_published == True)
    
    if category_id:
        query = query.filter(Post.category_id == category_id)
    
    posts = query.offset(skip).limit(limit).all()
    return posts

# Category Views
@router.get("/categories/", response_model=List[CategorySerializer])
async def list_categories_view(db: Session = Depends(get_db)):
    """List all categories"""
    categories = db.query(Category).all()
    return categories

@router.post("/categories/", response_model=CategorySerializer)
async def create_category_view(category: CategorySerializer, db: Session = Depends(get_db)):
    """Create a new category"""
    db_category = Category(**category.dict(exclude={'id'}))
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category