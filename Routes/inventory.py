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


inventoryData : List[schemas.InventoryInsights] = [
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-10-10', '%Y-%m-%d'), product_id=1),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-10-11', '%Y-%m-%d'), product_id=2),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-08-08', '%Y-%m-%d'), product_id=3),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-10-09', '%Y-%m-%d'), product_id=4),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-08-10', '%Y-%m-%d'), product_id=5),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-10-11', '%Y-%m-%d'), product_id=6),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-10-28', '%Y-%m-%d'), product_id=7),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-10-24', '%Y-%m-%d'), product_id=8),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-11-15', '%Y-%m-%d'), product_id=9),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-09-08', '%Y-%m-%d'), product_id=10),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-08-15', '%Y-%m-%d'), product_id=11),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-08-15', '%Y-%m-%d'), product_id=12),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-08-24', '%Y-%m-%d'), product_id=13),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-07-19', '%Y-%m-%d'), product_id=14),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-11-18', '%Y-%m-%d'), product_id=15),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-10-20', '%Y-%m-%d'), product_id=16),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-09-20', '%Y-%m-%d'), product_id=17),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-08-10', '%Y-%m-%d'), product_id=18),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-10-18', '%Y-%m-%d'), product_id=19),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-10-17', '%Y-%m-%d'), product_id=20),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-09-11', '%Y-%m-%d'), product_id=21),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-09-11', '%Y-%m-%d'), product_id=22),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-07-19', '%Y-%m-%d'), product_id=23),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-07-28', '%Y-%m-%d'), product_id=24),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-07-22', '%Y-%m-%d'), product_id=25),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-11-21', '%Y-%m-%d'), product_id=26),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-08-20', '%Y-%m-%d'), product_id=27),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-07-29', '%Y-%m-%d'), product_id=28),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-08-29', '%Y-%m-%d'), product_id=29),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-11-30', '%Y-%m-%d'), product_id=30),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-10-18', '%Y-%m-%d'), product_id=31),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-09-07', '%Y-%m-%d'), product_id=32),
    schemas.InventoryInsights(quantity=10, date= datetime.strptime('2023-08-05', '%Y-%m-%d'), product_id=33),
]

@router.post("/dumpinventory")
async def dumpInventory(db: db_dependency):
    try:
        for inventory in inventoryData:
            randomQuantity = random.randint(5,30)
            inventory.quantity = randomQuantity
            inventory_model = models.InventoryInsights(**inventory.dict())
            syncwithInventory(inventory_model.product_id, inventory_model.quantity,db)
            db.add(inventory_model)
        db.commit()
    except Exception as e:
        return {f"Error encountered while dumping inventory, {e}"}
    else: 
        return {
            "message":"Inventory Insights dumped Successfully",
            "count": len(inventoryData)
        }

@router.get("/inventoryinsigts")
async def getInventory(db: db_dependency):
    inventory = db.query(models.InventoryInsights).all()
    return inventory

@router.get("/inventory")
async def getInventory(db: db_dependency):
    inventory = db.query(models.Inventory).all()
    inventory_list = [{'productID': x.product_id,  'quantity': x.stock } for x in inventory]
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
