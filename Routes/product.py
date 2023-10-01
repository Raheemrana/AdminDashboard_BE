from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List
from sqlalchemy.orm import Session, joinedload
from database import get_db
import schemas
import models

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter()

@router.post("/product")
async def postProduct(name: str, db: db_dependency):
    product = schemas.Product(name="Ketchup", price=45, category_id=2)
    db.add(models.Product(**product.dict()))
    db.commit()
    return name

@router.get("/products")
async def getProducts(db: db_dependency):
    return db.query(models.Product).all()

@router.get("/products/{id}", status_code=200)
async def getProductByID(id:int, db: db_dependency):
    product = db.query(models.Product).filter_by(id = id).first()
    if product is None:
        raise HTTPException(status_code=400, detail="Product Not Found")
    return {"productName": product.name, "categoryName": product.category.name}