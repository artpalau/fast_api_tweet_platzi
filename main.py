## Python
from uuid import UUID
from datetime import date
from typing import Optional
from datetime import datetime

## Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

## FastApi
from fastapi import FastAPI

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

@app.get(
    path="/",
    summary="Home"
)
def home():
    return {"Twitter": "This is working"}