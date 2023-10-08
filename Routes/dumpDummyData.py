from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List
from sqlalchemy.orm import Session, joinedload
from database import get_db
import schemas
import models
from . import dummyData
from . import sale

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(tags=["Dump Dummy Data"])

@router.post("/dump-dummy-data")
async def dumpDummyData(db: db_dependency):
    try:
        # categories
        for category in dummyData.categoriesData:
            modelCategory = models.Category(**category.dict())
            db.add(modelCategory)
        db.commit()

        # products
        for product in dummyData.productsData:
            categoryId = db.query(models.Category).filter_by(name = product.category_name).first().id
            if categoryId == None:
                print(f"{categoryId}, doesn't exist")
                continue
            productModel = models.Product(name = product.name, price=product.price, category_id= categoryId)
            db.add(productModel)
            db.commit()
            db.add(models.Inventory(product_id= product.id, stock = 0))
            db.commit()

        # customers
        for customer in dummyData.customersData:
            db.add(models.Customer(**customer.dict()))
        db.commit()

        # sales
        sale.dumpData(db)

    except Exception as e:
        return {f"Error encountered while dumping data, error = {e}"}
    else: 
        return {
            "message":"Data has been dumped Successfully",
        }