# schemas.py
from datetime import datetime
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
    category_id: int | None = None
    category_name: str | None = None

    class Config:
        orm_mode = True


class InventoryInsights(BaseModel):
    product_id: int
    quantity: int
    date: datetime | None = None

    class Config:
        orm_mode = True