from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import Body, Query, Path

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
    name: Optional[str] = Query(
        None,
        min_length=2,
        max_length=50,
        title="Person Name",
        description="This is the person name. It´s between 2 and 50 characters"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It´s required"
        )
):
    return {name: age}

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This is the person ID, It´s required"
        )
):
    return {person_id: "It exists!"}