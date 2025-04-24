from fastapi import FastAPI
from .user.views import user_route
from .auth.views import auth_route


app = FastAPI()
app.include_router(user_route)
app.include_router(auth_route)