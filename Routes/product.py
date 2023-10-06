from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List
from sqlalchemy.orm import Session, joinedload
from database import get_db
import schemas
import models

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(tags=["Products"])

productsData : List[schemas.Product] = [
    schemas.Product(name="Bread", price=140, category_name="Bakery"),
    schemas.Product(name="Eggs", price=285, category_name="Bakery"),
    schemas.Product(name="Samosas", price=50, category_name="Bakery"),
    schemas.Product(name="Sandwich", price=100, category_name="Bakery"),
    schemas.Product(name="Juice", price=60, category_name="Bakery"),
    schemas.Product(name="Cake", price=750, category_name="Bakery"),
    schemas.Product(name="Rich Dad Poor Dad", price=245, category_name="Books and Magazines"),
    schemas.Product(name="Detectives", price=300, category_name="Books and Magazines"),
    schemas.Product(name="Animal Kingdom", price=350, category_name="Books and Magazines"),
    schemas.Product(name="Squid Games", price=200, category_name="Books and Magazines"),
    schemas.Product(name="History of Murders", price=225, category_name="Books and Magazines"),
    schemas.Product(name="Dasrk Side Of the Mind", price=310, category_name="Books and Magazines"),
    schemas.Product(name="Toy Story", price=270, category_name="Books and Magazines"),
    schemas.Product(name="Hoover", price=1500, category_name="Electronics"),
    schemas.Product(name="Kettle", price=2200, category_name="Electronics"),
    schemas.Product(name="Iron", price=1600, category_name="Electronics"),
    schemas.Product(name="LCD", price=8000, category_name="Electronics"),
    schemas.Product(name="Bulb", price=350, category_name="Electronics"),
    schemas.Product(name="Stove", price=4500, category_name="Electronics"),
    schemas.Product(name="Bat", price=1400, category_name="Sports"),
    schemas.Product(name="Baseball", price=850, category_name="Sports"),
    schemas.Product(name="Raquet", price=2200, category_name="Sports"),
    schemas.Product(name="Ball", price=110, category_name="Sports"),
    schemas.Product(name="Volley Ball", price=550, category_name="Sports"),
    schemas.Product(name="Sharp Knife", price=320, category_name="Gadgets"),
    schemas.Product(name="Small Projector", price=720, category_name="Gadgets"),
    schemas.Product(name="Bluetooth speaker", price=1050, category_name="Gadgets"),
    schemas.Product(name="Ear dots", price=1800, category_name="Gadgets"),
    schemas.Product(name="Handfrees", price=250, category_name="Gadgets"),
    schemas.Product(name="Jean", price=950, category_name="Clothing and Apparel"),
    schemas.Product(name="Shirt", price=500, category_name="Clothing and Apparel"),
    schemas.Product(name="Socks", price=230, category_name="Clothing and Apparel")
]

@router.post("/dumpproduct")
async def dumpProducts(db: db_dependency):
    try:
        counter: int = 0
        for product in productsData:
            categoryId = db.query(models.Category).filter_by(name = product.category_name).first().id
            if categoryId == None:
                print(f"{categoryId}, doesn't exist")
                continue
            counter =  counter + 1
            db.add(models.Product(name = product.name, price=product.price, category_id= categoryId))
        db.commit()
    except Exception as e:
        return {f"Error encountered while dumping products, {e}"}
    else: 
        return {
            "message":"Products dumped Successfully",
            "count": len(productsData)
        }

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