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
from fastapi import Body, Form, Path
from fastapi import HTTPException


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
    #response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    tags=["Users"]
)
def login(
    userLogin: UserLogin = Body(...)
):
    """
    Login

    This path operation lets you login to the app.

    Parameters:
        - user_id: UUID
        - email: Emailstr
        - password: str

    Returns:
        Returns confirmation that it is correct
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = userLogin.dict() 
        user_dict["user_id"] = str(user_dict["user_id"])
        for user_data in results:
            if user_data["user_id"] == user_dict["user_id"]:
                if user_data["email"] == user_dict["email"]:
                    if user_data["password"] == user_dict["password"]:
                        return {"login": "successful"}
                    else: {"something": "was incorrect"}
            
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
def display_user(
    user_id: str = Path(..., min_length=1)
):
    """
    Display single user data

    This path operation will display a single user from the app.

    Parameters:
        - userid : str

    Returns: Returns json list with the user in the app, with the following data:
        - user_id: UUID
        - email: Emailstr
        - firstName: str
        - lastName: str
        - birth_date: date

    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_found = False
        for user_data in results:
            if user_data["user_id"] == user_id:
                user_found = True
                break
        if user_found == True:
            return user_data
        else:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This id does not exist"
        )
    
### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    #response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"]
)
def delete_user(
    user_id: str = Path(..., min_length=1)
):
    """
    Delete single user data

    This path operation will delete a single user from the app.

    Parameters:
        - userid : str

    Returns: Returns a confirmation of what id was deleted

    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_found = False
        for i in range(len(results)):
            if results[i]["user_id"] == user_id:
                user_found = True
                break
        if user_found == True:
            del results[i]
        else:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This id does not exist"
            )
        f.truncate(0)
        f.seek(0)
        f.write(json.dumps(results))
        return {"user id deleted": user_id}

### Update a user
@app.put(
    path="/users/{user_id}/update",
    #response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["Users"]
)
def update_user(
    user_id: str = Path(..., min_length=1),
    email: Optional[str] = Form(default=None),
    firstName: Optional[str] = Form(default=None),
    lastName: Optional[str] = Form(default=None),
    birth_date: Optional[str] = Form(default=None)
): 
    """
    Update single user data

    This path operation will update a single users data from the app.

    Parameters:
        - userid : str
        - email: str, optional
        - firstName: str, optional
        - lastName: str, optional
        - birth_date: str, optional

    Returns: Returns json list with the user deleted from the app, with the following data:
        - user_id: UUID
        - email: Emailstr
        - firstName: str
        - lastName: str
        - birth_date: date

    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_found = False
        for i in range(len(results)):
            if results[i]["user_id"] == user_id:
                user_found = True
                break
        if user_found == True:
            if email: results[i]["email"] = email
            if firstName: results[i]["firstName"] = firstName
            if lastName: results[i]["lastName"] = lastName
            if birth_date: results[i]["birth_date"] = birth_date
        else:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This id does not exist"
            )
        f.truncate(0)
        f.seek(0)
        f.write(json.dumps(results))
        return {"user id is updated": user_id}
    
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
    """
    Display all tweets in app

    This path operation will display all tweets in the app.

    Parameters:
        -

    Returns: Returns json list with all tweets in the app, with the following data:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: datetime, optional
        - by: User

    """
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=['Tweets']
)
def post(
    tweet: Tweet = Body(...)
):
    """
    Post a tweet

    This path operation posts a tweet in the app.

    Parameters:
        - Request body parameter
            - Tweet

    Return: Returns a json with the basic tweet information:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: datetime, optional
        - by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        if tweet_dict["updated_at"]: tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet     

### Display a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Display a tweet",
    tags=['Tweets']
)
def display_tweet(
    tweet_id: str = Path(..., min_length=1)
):
    """
    Display single tweet in the app

    This path operation will display a single tweet in the app.

    Parameters:
        - tweet_id : str

    Returns: Returns json list with the tweet in the app, with the following data:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: datetime, optional
        - by: User

    """
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_found = False
        for tweet_data in results:
            if tweet_data["tweet_id"] == tweet_id:
                tweet_found = True
                break
        if tweet_found == True:
            return tweet_data
        else:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This id does not exist"
        )

### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    #response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=['Tweets']
)
def delete_tweet(
    tweet_id: str = Path(..., min_length=1)
):
    """
    Delete single tweet data

    This path operation will delete a single tweet from the app.

    Parameters:
        - tweet_id : str

    Return: Returns a json with the basic tweet information:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: datetime, optional
        - by: User

    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_found = False
        for i in range(len(results)):
            if results[i]["tweet_id"] == tweet_id:
                tweet_found = True
                break
        if tweet_found == True:
            del results[i]
        else:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This id does not exist"
            )
        f.truncate(0)
        f.seek(0)
        f.write(json.dumps(results))
        return {"user id deleted": tweet_id}

### Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    #response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=['Tweets']
)
def update_tweet(
    tweet_id: str = Path(..., min_length=1),
    content: str = Form(..., min_length=1),
    updated_at: datetime = Form(default=datetime.now())
):
    """
    Update single tweet data

    This path operation will update a single tweet from the app.

    Parameters:
        - tweet_id : str
        - content: str
        - updated_at: datetime

    Return: Returns a json with the basic tweet information:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: datetime, optional
        - by: User

    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_found = False
        for i in range(len(results)):
            if results[i]["tweet_id"] == tweet_id:
                tweet_found = True
                break
        if tweet_found == True:
            updated_at= str(updated_at)
            results[i]["content"] = content
            results[i]["updated_at"] = updated_at
        else:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This id does not exist"
            )
        f.truncate(0)
        f.seek(0)
        f.write(json.dumps(results))
        return {"user id is updated": tweet_id}
