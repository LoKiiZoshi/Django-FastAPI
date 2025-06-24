import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from asgiref.wsgi import WsgiToAsgi
from starlette.middleware import Middleware  # Fallback import

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_fastapi_project.settings')

# Django ASGI application
django_application = get_asgi_application()

# Create FastAPI instancec   
fastapi_app = FastAPI()

# API Endpoints
@fastapi_app.get("/fastapi/")
async def read_root():
    return {"message": "Hello from FastAPI!"}

@fastapi_app.get("/fastapi/users/")
async def get_users():
    users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "LOKII"}]
    return {"users": users}

@fastapi_app.get("/fastapi/user/{user_id}")
async def get_user(user_id: int):
    users = {1: {"name": "Alice"}, 2: {"name": "LOKII"}}
    user = users.get(user_id)
    if user:
        return user
    return {"error": "User not found"}, 404

@fastapi_app.post("/fastapi/add_user/")
async def add_user(name: str):
    new_user = {"id": 3, "name": name}
    return {"message": "User added", "user": new_user}, 201

# Combine Django and FastAPI using Starlette middleware as a fallback
middleware = [Middleware(WsgiToAsgi, app=django_application)]
fastapi_app.add_middleware(WsgiToAsgi, app=django_application)
application = fastapi_app