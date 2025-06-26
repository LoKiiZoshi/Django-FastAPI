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