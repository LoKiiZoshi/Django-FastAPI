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