from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List
from sqlalchemy.orm import Session, joinedload
from database import get_db
import schemas
import models

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(tags=["Category"])

# this is the dummy data to load at first application run

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
    return f"{category.name} has been added successfully"

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
