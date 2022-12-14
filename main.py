## FastApi
from fastapi import FastAPI

app = FastAPI()

@app.get(
    path="/",
    summary="Home"
)
def home():
    return {"Twitter": "This is working"}