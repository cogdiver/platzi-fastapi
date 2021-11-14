# Python

# FastAPI
from fastapi import FastAPI

app = FastAPI()

@app.get(path="/")
def home():
    return {"Platzi":"It's Working"}


