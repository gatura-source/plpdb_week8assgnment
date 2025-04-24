from pydantic_settings import BaseSettings
from secrets import token_urlsafe
from dotenv import load_dotenv
import sys
import os


if not load_dotenv():
	sys.stdout.write("ENV files not loaded")

class Settings(BaseSettings):
    app_name: str = "FastAPI CRUD Application"
    secret_key: str = token_urlsafe(32)
    DATABASE_URI:str = f"mariadb+mariadbconnector://{os.getenv("DB_USER")}:"\
    f"{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}"
    debug: bool = False


settings = Settings()
