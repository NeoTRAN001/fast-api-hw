from typing import Optional
from enum import Enum
from pydantic import BaseModel
from pydantic import Field
from fastapi import FastAPI
from fastapi import Body, Query, Path
from pydantic.schema import schema

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    black = "black"
    brown = "brown"
    blonde = "blonde"
    red = "red"

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=50
        )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=50
        )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    password: str = Field(
        ...,
        min_length=8
        )

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Facundo",
                "last_name": "Loverte",
                "age": 21,
                "hair_color": "black",
                "is_married": False,
                "password": "123456789"
            }
        }

class PersonOuth(BaseModel):
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=50
        )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=50
        )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

class Location(BaseModel):
    city: str
    state: str
    country: str

# Routes
@app.get("/")
def home():
    return {
        "Hello": "World"
    }

@app.post("/person/new", response_model=PersonOuth)
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

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID, It´s required",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict()) # Combinar dos json

    return results