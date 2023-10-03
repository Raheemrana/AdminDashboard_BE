from typing import Annotated
from fastapi import Depends, FastAPI
from pydantic import BaseModel
import models
from database import db_engine, SessionLocal, get_db
from schemas import Customer
from sqlalchemy.orm import Session
from Routes import inventory, product, category, customer, sale
app = FastAPI()

models.Base.metadata.create_all(bind=db_engine)

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(inventory.router)
app.include_router(product.router)
app.include_router(category.router)
app.include_router(customer.router)
app.include_router(sale.router)
