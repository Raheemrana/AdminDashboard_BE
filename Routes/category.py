from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List
from sqlalchemy.orm import Session, joinedload
from database import get_db
import schemas
import models

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(tags=["Category"])
    
categoriesData: List[schemas.Category] = [
    schemas.Category(name="Bakery"),
    schemas.Category(name="Books and Magazines"),
    schemas.Category(name="Electronics"),
    schemas.Category(name="Sports"),
    schemas.Category(name="Gadgets"),
    schemas.Category(name="Clothing and Apparel")

]

@router.post("/dumpcategories")
async def dumpCategories(db: db_dependency):
    try:
        for category in categoriesData:
            modelCategory = models.Category(**category.dict())
            db.add(modelCategory)
        db.commit()
    except Exception as e:
        return {f"Error encountered while dumping categories, {e}"}
    else: 
        return {
            "message":"Categories dumped Successfully",
            "count": len(categoriesData)
        }

@router.get("/categories")
async def getCategories(db: db_dependency):
    categories = db.query(models.Category).\
    all()
    # options(joinedload(models.Category.products)).\
    return categories

@router.post("/category")
async def postCategory(category:schemas.Category, db: db_dependency):
    modelCategory = models.Category(**category.dict())
    db.add(modelCategory)
    db.commit()
    return modelCategory.id

@router.delete("/category")
async def deleteCategories(name: str, db: db_dependency):
    category_to_delete = db.query(models.Category).filter(models.Category.name == name).first()
    if category_to_delete:
        db.delete(category_to_delete)
        db.commit()
        return f"{name} category has been deleted"
    else:
        return f"Category with name {name} not found"

@router.get("/categories-dropdown")
async def getCategoriesDropdown(db: db_dependency):
    return db.query(models.Category.id.label('key'),models.Category.name.label('value')).all()
