from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List
from sqlalchemy import func, update
from sqlalchemy.orm import Session, joinedload
from database import get_db
import schemas
import models
import random

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(tags=["Inventory"])

@router.post("/dumpinventory")
async def dumpInventory(db: db_dependency):
    try:
        count = random.randint()
        for count in range(0,count):
            # any random product among 33 products
            randomProduct = random.randint(1,33)
            # random quantity for each inventory
            randomQuantity = random.randint(5,30)
            #random date
            randomDatestring = '2023' + random.randint(1,12) + random.randint(1,30)
            randomDate = datetime.strptime(randomDatestring, '%Y-%m-%d')
            
            inventory_model = models.InventoryInsights(product_id=randomProduct, quantity=randomQuantity, date=randomDate)
            # synchronize with Inventory table that has total count of each product
            syncwithInventory(inventory_model.product_id, inventory_model.quantity, db)
            db.add(inventory_model)
        db.commit()
    except Exception as e:
        return {f"Error encountered while dumping inventory, {e}"}
    else: 
        return {
            "message":"Inventory Insights dumped Successfully",
            "count": len(count)
        }


@router.get("/inventoryinsigts")
async def getInventory(db: db_dependency):
    inventory = db.query(models.InventoryInsights).all()
    return inventory

@router.get("/inventory")
async def getInventory(db: db_dependency):
    inventory = db.query(models.Inventory).options(joinedload(models.Inventory.product)).all()
    inventory_list = [{'productID': x.product_id, 'productName':x.product.name,  'quantity': x.stock } for x in inventory]
    return inventory_list

def syncwithInventory(productID: int, quantity: int, db: db_dependency):
    inventory = db.query(models.Inventory).filter_by(product_id = productID).first()
    if inventory == None:
        print(f"Adding Inventory for product id {productID}")
        db.add(models.Inventory(product_id = productID, stock = quantity))
    else:
        update_query = update(models.Inventory).filter_by(product_id = productID).values({models.Inventory.stock: inventory.stock + quantity})
        db.execute(update_query)
    db.commit()
    
@router.post("/inventoryinsights")
async def postInventoryInsights(data: schemas.InventoryInsights, db: db_dependency):
    if data == None:
        return "Null object received"
    if data.date == None:
        data.date = datetime.strptime(str(datetime.today().date()), '%Y-%m-%d')
    inventory_model = models.InventoryInsights(**data.dict())
    syncwithInventory(inventory_model.product_id, inventory_model.quantity, db)
    db.add(inventory_model)
    db.commit()

@router.get("/totalInventory")
async def totalInventory(db:db_dependency):
    total_inventory = db.query(func.sum(models.Inventory.stock)).scalar()
    total_products = db.query(func.count(models.Inventory.product_id.distinct())).scalar()
    return { 'products': total_products, 'total_stock':total_inventory }
