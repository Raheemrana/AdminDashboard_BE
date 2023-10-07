from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List
from sqlalchemy.orm import Session, joinedload
from database import get_db
import schemas
import models

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(tags=["Products"])


@router.post("/product")
async def postProduct(name: str, price: int, category_id: int, db: db_dependency):
    db.add(models.Product(name= name, price=price, category_id=category_id))
    db.commit()
    return name + " product successfully added"

@router.get("/products")
async def getProducts(db: db_dependency):
    products = db.query(models.Product).options(joinedload(models.Product.category)).all()
    results = [
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "category_name": product.category.name if product.category else None
        }
        for product in products
    ]
    return results

@router.get("/products/{id}", status_code=200)
async def getProductByID(id:int, db: db_dependency):
    product = db.query(models.Product).filter_by(id = id).first()
    if product is None:
        raise HTTPException(status_code=400, detail="Product Not Found")
    return {"productName": product.name, "categoryName": product.category.name}


@router.get("/products-dropdown")
async def getProductsDropdown(db: db_dependency):
    return db.query(models.Product.id.label('key'),models.Product.name.label('value')).all()