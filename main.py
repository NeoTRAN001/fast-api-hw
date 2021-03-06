from typing import Optional
from enum import Enum
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, File, UploadFile

app = FastAPI()

# Models
class HairColor(Enum):
    white = "white"
    black = "black"
    brown = "brown"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str
    state: str
    country: str

class PersonBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., gt=0,le=115)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

class Person(PersonBase):
    password: str = Field(...,min_length=8)
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

class PersonOuth(PersonBase):
    pass

class LoginOuth(BaseModel):
    username: str = Field(..., min_length=1, max_length=20, example="neotran")
    message: str = Field(default="Login Succesfully")

# Routes
@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Home"]
)
def home():
    """Esto es una documentación de prueba en el home"""
    return {
        "Hello": "World"
    }

@app.post(
    path="/person/new",
    response_model=PersonOuth,
    status_code=status.HTTP_201_CREATED,
    tags=["Person"],
    summary="Create Person in the app"
)
def create_person(person: Person = Body(...)):
    """
    ## Create Person
    This path operation creates a person in the app and save the information in the dadabase
    
    Parameters:
    - Request body parameter:
        - **person: Person** -> A person model with first name, lastname, age, hair color and married

    Returns a person model with first name, last name, age, hair color and married
    """
    return person

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Person"],
    deprecated=True
)
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

persons = [1,2,3,4,5]

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Person"]
)
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This is the person ID, It´s required",
        example="2"
        )
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This person doesn´t exist!"
        )
    return {person_id: "It exists!"}

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Person"]
)
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

# Forms
@app.post(
    path="/login",
    response_model=LoginOuth,
    status_code=status.HTTP_200_OK,
    tags=["Login"]
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOuth(username=username)

# Cookies and Headers Parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Contacts"]
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

# Files and Uploadfile
@app.post(
    path="/post-image",
    tags=["Files"]
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read()) / 1024, ndigits=2)
    }