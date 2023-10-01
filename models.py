from enum import Enum
from sqlalchemy import Column, Date, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#   enums
class Gender(str, Enum):
    Make = "Make"
    Female = "Female"

class Transation(str, Enum):
    Online = "Online"
    InShop = "InShop"

#   models 

class Identity(Base):
    id = Column(Integer, primary_key=True)

class Customer(Identity):
    __tablename__ = 'customer'
    name = Column(String, unique=True, nullable=False)
    gender = Column(Enum(Gender, nullable=False))
    age = Column(Integer, nullable=False)
    phone = Column(Integer)

class Category(Identity):
    __tablename__ = 'category'
    name = Column(String, unique=True, nullable=False)

class Product(Identity):
    __tablename__ = 'product'
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)

class Sales(Identity):
    __tablename__ = 'sales'
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)

class Invoice(Identity):
    __tablename__ = 'invoice'
    transaction_type = Column(Enum(Transation))
    amount = Column(Float, nullable=False)
    date = Column(Date)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)

class Inventory(Identity):
    __tablename__ = 'inventory'
    stock = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)

class InventoryInsights(Identity):
    __tablename__ = 'inventoryinsights'
    quantity = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)



