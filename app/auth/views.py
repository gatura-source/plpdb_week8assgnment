from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from sqlalchemy import text
from . import generate_token
from pydantic import BaseModel


auth_route = APIRouter()

class Person(BaseModel):
    username: str

@auth_route.post('/auth/login')
def hello(person: Person, db: Session = Depends(get_db)):
    result = db.execute(text(f"SELECT * FROM users WHERE username = '{person.username}'"))
    row = result.fetchone()._asdict()
    if row is not None and len(row) != 0:
        return (f"Auth Token: {generate_token({"sub": row["username"]})}")
    else:
        return (f"User {person.username} Not Found")
    
