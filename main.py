## Python
import json
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
from fastapi import Body

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

class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8
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

## Users

### Register a User
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Sign up a new user",
    tags=["Users"]
)
def signup(
    user: UserRegister = Body(...)
):
    """
    Register a User

    This path operation registers a user in the app.

    Parameters:
        - Request body parameter
            - UserRegister

    Return: Returns a json with the basic user information:
        - user_id: UUID
        - email: Emailstr
        - firstName: str
        - lastName: str
        - birth_date: date
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user

### Login with a User
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    tags=["Users"]
)
def login():
    pass

### Display all Users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Display all users",
    tags=["Users"]
)
def display_all_users():
    """
    Display all users in db

    This path operation will display all users in the app.

    Parameters:
        -

    Returns: Returns json list with all users in the app, with the following data:
        - user_id: UUID
        - email: Emailstr
        - firstName: str
        - lastName: str
        - birth_date: date

    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Display a single uer
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Display a user",
    tags=["Users"]
)
def display_user():
    pass

### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"]
)
def delete_user():
    pass

### Update a user
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

### Display all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Home, display all Tweets",
    tags=['Tweets']
)
def home():
    return {"Twitter": "This is working"}

### Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=['Tweets']
)
def post():
    pass

### Display a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Display a tweet",
    tags=['Tweets']
)
def post():
    pass

### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=['Tweets']
)
def post():
    pass

### Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=['Tweets']
)
def post():
    pass
