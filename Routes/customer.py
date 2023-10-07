from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(tags=["Customer"])

@router.post("/customer")
async def postCustomer(data:schemas.Customer, db: db_dependency):
    db.add(models.Customer(**data.dict()))
    db.commit()
    return f"Customer {data.name} has been added"

@router.get("/customers")
async def getCustomers(db: db_dependency):
    customers = db.query(models.Customer.id, models.Customer.name, models.Customer.age, models.Customer.gender).all()
    return customers

@router.get("/customer/{id}")
async def getCustomer(id: int, db: db_dependency):
    customername = db.query(models.Customer.name.label('Customer Name'))\
    .filter_by(id = id).first()
    return customername
