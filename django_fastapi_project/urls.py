from fastapi import APIRouter
from core.urls import router as core_router

# Main API router
api_router = APIRouter(prefix="/api/v1")

# Include app routers
api_router.include_router(core_router, prefix="/core", tags=["core"])

# URL patterns for reference
urlpatterns = [
    # Core app URLs
    {"path": "/api/v1/core/users/", "name": "user-list"},
    {"path": "/api/v1/core/users/{id}/", "name": "user-detail"},
    {"path": "/api/v1/core/posts/", "name": "post-list"},
    {"path": "/api/v1/core/posts/{id}/", "name": "post-detail"},
    {"path": "/api/v1/core/categories/", "name": "category-list"},
    
    # Admin URLs
    {"path": "/admin/", "name": "admin"},
    
    # Health check
    {"path": "/health/", "name": "health-check"},
]
