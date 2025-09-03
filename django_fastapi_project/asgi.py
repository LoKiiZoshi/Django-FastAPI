import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
from fastapi_app.main import fastapi_app


os.environ.setdefault("DJANGO_SETTING_MODULE","django_fastapi_project.settings")


#Django ASGI app 

django_app = get_asgi_application()

#Mount Django inside FastAPI

fastapi_app.mount("/django",WSGIMiddleware(django_app))

#Uvicorn will use this


application = fastapi_app

