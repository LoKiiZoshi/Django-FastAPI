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