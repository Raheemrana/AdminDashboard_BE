# schemas.py
from pydantic import BaseModel


class Customer(BaseModel):
    name: str
    age: int
    phone: int

    class Config:
        orm_mode = True

class Category(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Product(BaseModel):
    name: str
    price: int
    category_id: int

    class Config:
        orm_mode = True