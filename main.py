## Python
from uuid import UUID
from datetime import date
from typing import Optional, List
from datetime import datetime

## Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

## FastApi
from fastapi import FastAPI
from fastapi import status

app = FastAPI()

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)
    
class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8
    )

class User(UserBase):
    firstName: str = Field(
        ...,
        min_length=1,
        max_length=20
        )
    lastName: str = Field(
        ...,
        min_length=1,
        max_length=20
        )
    birth_date: Optional[date] = Field(
        default=None
    )

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)

# Path Operations

@app.get(
    path="/",
    summary="Home"
)
def home():
    return {"Twitter": "This is working"}

## Users

@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Sign up a new user",
    tags=["Users"]
)
def signup():
    pass

@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    tags=["Users"]
)
def login():
    pass

@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Display all users",
    tags=["Users"]
)
def display_all_users():
    pass

@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Display a user",
    tags=["Users"]
)
def display_user():
    pass

@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"]
)
def delete_user():
    pass

@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["Users"]
)
def update_user():
    pass

## Tweets

