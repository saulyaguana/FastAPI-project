#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field, EmailStr

#FastApi
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
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
    status_code=status.HTTP_200_OK,
    tags=["Home"],
    summary="Home Start"
    )
def home():
    """
    ->Home Start

    ->This path operation just salute an user

    ->This path operation doens't have a parameters

    ->This path operation just returns a message that salute an user
    """
    return {"hello": "David"}

#Request and Responde Body

@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create Person in the app."
    )
def create_person(people: Person = Body(...)):
    """
    ->Titulo: Create Person in the app

    ->Descripcion: This path operation creates a person in the app

    and save the information in the database

    ->Parametros:

    -Request Body Parameter:

        -**person: Person** -> A person model with first name, last name, age, hair color and marital state

    ->Resultado:

    Returns a person model with first name, last name, age, hair color and marital state
    """
    return people

#Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Show Person Data",
    deprecated=True
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
    """
    ->Show Person Data

    ->This path operation creates a data from an user

    ->Parameters:

        -**name: str** -> an optional query parameter parameter to know the person name

        -**age: int** -> an optinal query parameter parameter to know the person age
    
    ->This path operation returns in json format the name as a key and the age as a value.
    """
    return {name: age}

# Validaciones: Path Parameters

persons = list(range(1, 101))

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Show Person Id"
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
    """
    Show Person Id

    This path operation creates the id of an user

    Parameters:

        -**person_id: int** -> an obligatory path parameter to know the id user.
    
    Returns the id user in a json but if the id doensn't exist it will raise an HTTPException error
    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doensn't exist."
        )
    return {person_id: "Right"}

# Validaciones: Request Body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_100_CONTINUE,
    tags=["Persons"],
    summary="Update an User"
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
    """
    Update an User

    This path operation update an user id

    ->Parameters:

        -**person_id: int** -> An obligatory path parameter to know the person id.
        -**place: Location** -> An Location model with city, state and country

    Returns Location model with city, state and country
    """
    #result = person_body.dict()
    #result.update(place.dict())
    #return result 
    return place

#Forms
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Secure Login"
)
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    """
    Secure Login

    This path operation create an username and password

    ->Parameters:
    
        -**username: str** -> A Form with username
        -**password: str** -> A Form with password

    Returns a Loging out model only with the username and a message.
    """
    return LoginOut(username=username)


#Cookies and Headers Parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Info"],
    summary="Contact"
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
    """
    Contact

    This path operation save in database the information in Form format.

    Parameters:

        -**first_name: str** -> A Form format to know the name
        -**last_name: str** -> A Form format to know the last name
        -**email: EmailStr** -> A Form format to know the email from the user
        -**message: str** -> A Form format to know the message from the user
        -**user_agent: str** -> An optional Header to know this data
        -**ads: str** -> An optional Cookie to know this data

    Returns user_agent
    """
    return user_agent


#Files
@app.post(
    path="/post-image",
    status_code=status.HTTP_200_OK,
    tags=["Multimedia"],
    summary="Multimedia"
)
def post_image(
    image: UploadFile = File(...)
):
    """
    Multimedia

    This path operation is to upload a file

    parameters:

        -**image: UploadFile** -> A UploadFile class with some atributes

    Returns a json format with atributes from the class UploadFile
    """
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=3)
    }