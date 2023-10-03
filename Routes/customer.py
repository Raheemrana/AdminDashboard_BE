from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(tags=["Customer"])

customersData : List[schemas.Customer] = [
    schemas.Customer(name= "Shastri", age= 27, gender= models.Gender.Male),
    schemas.Customer(name= "Arjun", age= 27, gender= models.Gender.Male),
    schemas.Customer(name= "Miley", age= 23, gender= models.Gender.Female),
    schemas.Customer(name= "Arnold", age= 52, gender= models.Gender.Male),
    schemas.Customer(name= "Kanya", age= 22, gender= models.Gender.Male),
    schemas.Customer(name= "Hadid", age= 24, gender= models.Gender.Female),
    schemas.Customer(name= "Hanabel", age= 30, gender= models.Gender.Male),
    schemas.Customer(name= "Taylor", age= 31, gender= models.Gender.Female),
    schemas.Customer(name= "Niki", age= 42, gender= models.Gender.Female),
    schemas.Customer(name= "Kylie", age= 35, gender= models.Gender.Female),
]

@router.post("/dumpcustomers")
async def dumpCustomers(db:db_dependency):
    try:
        for customer in customersData:
            db.add(models.Customer(**customer.dict()))
        db.commit()
    except Exception as e:
        return {f"Error encountered while dumping customers, {e}"}
    else: 
        return {
            "message":"Customers Insights dumped Successfully",
            "count": len(customersData)
        }

@router.post("/customer")
async def postCustomer(data:schemas.Customer, db: db_dependency):
    db.add(models.Customer(**data.dict()))
    db.commit()
    return f"Customer {data.name} has been added"

@router.get("/customers")
async def getCustomers(db: db_dependency):
    customers = db.query(models.Customer).all()
    return customers

@router.get("/customer/{id}")
async def getCustomer(id: int, db: db_dependency):
    customername = db.query(models.Customer.name.label('Customer Name'))\
    .filter_by(id = id).first()
    return customername
