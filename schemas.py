# schemas.py
from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel

from models import Gender, Transation


class Customer(BaseModel):
    name: str
    age: int
    phone: int | None = None
    gender: Gender

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

class Sale (BaseModel):
    product_name: str
    quantity: int
    total_price: float | None
    product_id: int | None

class Receipt(BaseModel):
    transaction_type: Transation
    customer_name: str
    date: datetime | None = None
    sales: List[Sale]


    class Config:
        orm_mode = True