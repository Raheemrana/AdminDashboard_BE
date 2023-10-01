from enum import Enum as PyEnum
from sqlalchemy import Column, Date, Float, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base

#   enums
class Gender(PyEnum):
    Make = "Make"
    Female = "Female"

class Transation(PyEnum):
    Online = "Online"
    InShop = "InShop"

#   models 
    

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255), unique=True, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(Integer)
    invoices = relationship("Invoice", back_populates="customer")

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255), unique=True, nullable=False)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255), unique=True, nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    sales = relationship("Sales", back_populates="product")
    inventory = relationship("Inventory",uselist=False, back_populates="product")
    inventoryinsights = relationship("InventoryInsights", back_populates="product")
    category = relationship("Category", back_populates="products")

class Sales(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    invoice_id = Column(Integer, ForeignKey('invoice.id'), nullable=False)
    product = relationship("Product", back_populates="sales")
    invoice = relationship("Invoice", back_populates="sales")

class Invoice(Base):
    __tablename__ = 'invoice'
    id = Column(Integer, primary_key=True)
    transaction_type = Column(Enum(Transation))
    amount = Column(Float, nullable=False)
    date = Column(Date)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    customer = relationship("Customer", back_populates="invoices")
    sales = relationship("Sales", back_populates="invoice")

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    stock = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), unique=True ,nullable=False)
    product = relationship("Product", back_populates="inventory")


class InventoryInsights(Base):
    __tablename__ = 'inventoryinsights'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    product = relationship("Product", back_populates="inventoryinsights")


