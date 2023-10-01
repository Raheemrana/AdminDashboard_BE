from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List
from sqlalchemy.orm import Session, joinedload
from database import get_db
import schemas
import models

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter()
    

@router.get("/categories")
async def getCategories(db: db_dependency):
    categories = db.query(models.Category).options(joinedload(models.Category.products)).all()
    return categories

@router.post("/category")
async def postCategory(category:schemas.Category, db: db_dependency):
    modelCategory = models.Category(**category.dict())
    db.add(modelCategory)
    db.commit()
    return modelCategory

@router.post("/categories")
async def postCategories(names:List[str], db: db_dependency):
    for name in names:
        category = schemas.Category(name = name)
        modelCategory = models.Category(**category.dict())
        db.add(modelCategory)
    db.commit()
    return names
