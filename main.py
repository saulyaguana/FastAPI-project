#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field, EmailStr

#FastApi
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File

app = FastAPI()

#Models
class Countrys(Enum):
    Ecuador = "Ecuador"
    Argelia = "Argelia"
    Holanda = "Holanda"
    Dinamarca = "Dinamarca"
    Finlandia = "Finlandia"

class HairColor(Enum):
    white = "White"
    Black = "Black"
    Brown = "Brown"
    Yellow = "Blonde"
    Red = "Red"

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=30, #estos son parámetros
        title="City",
        description="City where you live",
        example="Amsterdam"
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=30,
        title="State",
        description="State where you live",
        example="State of Amsterdam"
    )
    country: Countrys = Field(...)

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    email: EmailStr = Field(...)


class Person(PersonBase):
    
    password: str = Field(..., min_length=8)
    class Config:
        schema_extra = {
            "example" : {
                "first_name": "Gideon",
                "last_name": "Emery",
                "age": 35,
                "hair_color": "Black",
                "is_married": True,
                "email": "joker@atlas.com",
                "password": "IworkinAtlasCorporation"
            }
        }

class PersonOut(PersonBase):
    pass

class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="gideon2054")
    message: str = Field(default="Login Succesfully!")

@app.get(
    path="/",
    status_code=status.HTTP_200_OK
    )
def home():
    return {"hello": "David"}

#Request and Responde Body

@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(people: Person = Body(...)):
    return people

#Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
    )
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Alan"
        ),
    age: int = Query(
        ...,
        ge=1,
        le=115,
        title="Person age",
        description="This is the person age. It's required",
        example=45
        )
):
    return {name: age}

# Validaciones: Path Parameters

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK
    )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This is the Person ID",
        example=117
        )
):
    return {person_id: "Right"}

# Validaciones: Request Body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_100_CONTINUE
    )
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the Person ID",
        gt=0,
        example=609
    ),
    #person_body: Person = Body(...),
    place: Location = Body(...),
):
    #result = person_body.dict()
    #result.update(place.dict())
    #return result 
    return place

#Forms
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    return LoginOut(username=username)


#Cookies and Headers Parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
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
        min_length=20,
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent


#Files
@app.post(
    path="/post-image"
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=3)
    }

