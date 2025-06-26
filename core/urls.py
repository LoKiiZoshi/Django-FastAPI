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