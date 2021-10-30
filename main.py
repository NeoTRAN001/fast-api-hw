from typing import Optional
from fastapi.datastructures import Default
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import Body, Query

app = FastAPI()

# Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

# Routes
@app.get("/")
def home():
    return {
        "Hello": "World"
    }

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(None, min_length=2, max_length=50),
    age: str = Query(...)
):
    return {name: age}