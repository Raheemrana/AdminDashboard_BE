from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    age: int 
    address: str | None = None
    
MyUsers = []

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/users")
async def postUsers(user: Item):
    MyUsers.append(user)
    return {"user": user}

@app.get("/users")
async def getUsers():
    return MyUsers

@app.get("/users/{index}")
async def getUser(index:int):
    return {"user 3": MyUsers[index]}
