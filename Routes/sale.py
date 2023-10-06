from datetime import datetime
from enum import Enum
import random
import traceback
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List
from sqlalchemy import extract, func
from sqlalchemy.orm import Session, joinedload
from database import get_db
import schemas
import models
from . import customer
from . import product

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(tags=["Sales"])

# lets do it
customersNames = [x.name for x in customer.customersData]
productNames = [x.name for x in product.productsData]
invoicesList : schemas.Receipt = []
total_sales = 0
class spanType(Enum):
    day = "day"
    month = "month"
    year = "year"


@router.post("/dumpSales")
async def dumpSales(db:db_dependency):
    try:
        makeRandomSales()
        dumpRandomsales(db)
    except Exception as e:
        return {f"Error encountered while dumping invoices and sales, {e}"}
    else: 
        response = {
            "message":"Inventory Insights dumped Successfully",
            "count": "Invoices = " + str(len(invoicesList)) + " Sales = " + str(total_sales)
        }
        return response

@router.get("/invoices")
async def getInvoices(db: db_dependency):
    return db.query(models.Invoice).options(joinedload(models.Invoice.sales).joinedload(models.Sales.product)).all()

@router.get("/sales")
async def getSales(db: db_dependency):
    return db.query(models.Sales).options(joinedload(models.Sales.product)).all()

@router.get("/salescount")
async def getSales(db: db_dependency):
    return db.query(func.count(models.Sales.id)).scalar()

@router.get("/totalrevenue")
async def getSales(db: db_dependency):
    return db.query(func.sum(models.Sales.total_price)).scalar()

@router.get("/sales-by-month")
async def get_sales_by_month(db: db_dependency):
    # Get sales data for the whole year divided by month
    sales_by_month = (
        db.query(
            extract('year', models.Sales.date).label('year'),
            extract('month', models.Sales.date).label('month'),
            func.sum(models.Sales.total_price).label('total_sales')
        )
        .filter(extract('year', models.Sales.date) == 2023)  # Specify the desired year
        .group_by(extract('year', models.Sales.date), extract('month', models.Sales.date))
        .order_by('year', 'month')
        .all()
    )
    return sales_by_month

@router.get("/sales-by-year")
async def get_sales_by_year(db: db_dependency):
    sales_by_year = (
        db.query(
            extract('year', models.Sales.date).label('year'),
            func.sum(models.Sales.total_price).label('total_sales')
        )
        .group_by(extract('year', models.Sales.date))
        .order_by('year')
        .all()
    )
    return sales_by_year

@router.get("/sales-by-gender")
async def get_sales_by_gender(db: db_dependency):
    sales_by_gender = db.query(models.Customer.gender.label("gender"), func.count(models.Sales.id).label("sales")).\
    join(models.Invoice, models.Customer.id == models.Invoice.customer_id).\
    join(models.Sales, models.Invoice.id == models.Sales.invoice_id).\
    group_by(models.Customer.gender).all()

    totalSales = sales_by_gender[0]["sales"] + sales_by_gender[1]["sales"]
    result = []
    genders = [x["gender"] for x in sales_by_gender]
    sales = [round(x["sales"]/totalSales * 100,1) for x in sales_by_gender]
    return {
        "labels": genders,
        "dataset": sales
    }

@router.get("/sales-by-age-brackets")
async def get_sales_by_age_brackets(db: db_dependency):
    # Define age brackets (adjust these according to your requirements)
    age_brackets = [
        {"min": 18, "max": 24, "label": "18-24"},
        {"min": 25, "max": 34, "label": "25-34"},
        {"min": 35, "max": 44, "label": "35-44"},
        {"min": 45, "max": 54, "label": "45-54"},
        {"min": 55, "max": 64, "label": "55-64"},
        {"min": 65, "max": 100, "label": "65+"}
    ]

    sales_by_age_brackets = []
    total_sales = 0

    # Query sales data and calculate sales by age brackets
    for bracket in age_brackets:
        min_age, max_age = bracket["min"], bracket["max"]
        sales_count = (
            db.query(func.count(models.Sales.id))
            .join(models.Invoice, models.Invoice.id == models.Sales.invoice_id)
            .join(models.Customer, models.Customer.id == models.Invoice.customer_id)
            .filter(models.Customer.age >= min_age)
            .filter(models.Customer.age <= max_age)
            .scalar()
        )
        total_sales += sales_count
        sales_by_age_brackets.append({"age_bracket": bracket["label"], "sales": sales_count})

    # Calculate sales percentage for each age bracket
    dataset = [
        round((sale["sales"] / total_sales) * 100, 1) if total_sales > 0 else 0
        for sale in sales_by_age_brackets
    ]

    # Extract age bracket labels
    labels = [bracket["age_bracket"] for bracket in sales_by_age_brackets]

    return {
        "labels": labels,
        "dataset": dataset
    }

@router.get("/sales-by-day")
async def get_sales_by_day(db: db_dependency):
    sales_by_day = (
        db.query(
            (models.Sales.date).label('day'),
            func.sum(models.Sales.total_price).label('total_sales')
        )
        .group_by(models.Sales.date)
        .order_by('day')
        .all()
    )
    return sales_by_day

@router.get("/sales-by-transaction")
async def get_sales_by_transaction(db: db_dependency):
    sales_by_transaction = (
        db.query(
            func.count(models.Sales.id).label('sales'),
            (models.Invoice.transaction_type).label('transaction_type')).\
            join(models.Invoice, models.Invoice.id == models.Sales.invoice_id)
        .group_by(models.Invoice.transaction_type)
        .order_by(models.Invoice.transaction_type)
        .all()
    )
    labels = [x["transaction_type"] for x in sales_by_transaction]
    sales = [x["sales"] for x in sales_by_transaction]
    return {
        "labels": labels,
        "dataset": sales
    }

@router.get("/sales-by-filters")
async def get_sales_by_filter(db: db_dependency,startDate: str | None = None, endDate: str | None = None, category_id: int = 0, product_id: int = 0, span: spanType | None = 'day'):
    
    if span == spanType.day:
        query = (
        db.query(
            func.date(models.Sales.date).label('date'),
            func.sum(models.Sales.total_price).label('total_sales'),
            func.count(models.Sales.id).label('sales_count'),
            func.sum(models.Sales.quantity).label('total_units'),
        )
        .join(models.Product, models.Sales.product_id == models.Product.id)
        .join(models.Category, models.Product.category_id == models.Category.id)
        .group_by( models.Sales.date)
        .order_by(models.Sales.date)
    )
    elif span == spanType.month:
        query = (
        db.query(
            extract('year', models.Sales.date).label('year'),
            extract('month', models.Sales.date).label('month'),
            func.sum(models.Sales.total_price).label('total_sales'),
            func.count(models.Sales.id).label('sales_count'),
            func.sum(models.Sales.quantity).label('total_units'),
        )
        .join(models.Product, models.Sales.product_id == models.Product.id)
        .join(models.Category, models.Product.category_id == models.Category.id)
        .group_by(extract('year', models.Sales.date), extract('month', models.Sales.date))
        .order_by('year', 'month')
    )
    else:
        query = (
        db.query(
            extract('year', models.Sales.date).label('year'),
            func.sum(models.Sales.total_price).label('total_sales'),
            func.count(models.Sales.id).label('sales_count'),
            func.sum(models.Sales.quantity).label('total_units'),
        )
        .join(models.Product, models.Sales.product_id == models.Product.id)
        .join(models.Category, models.Product.category_id == models.Category.id)
        .group_by(extract('year', models.Sales.date))
        .order_by('year')
    )
    
    if product_id > 0:
        query = query.filter(models.Sales.product_id == product_id)
    if category_id > 0:
        query = query.filter(models.Category.id == category_id) 
    if startDate is not None:
        startDate = datetime.strptime(startDate, '%Y-%m-%d')
        query = query.filter(models.Sales.date >= startDate)
    if endDate is not None:
        endDate = datetime.strptime(endDate, '%Y-%m-%d')
        query = query.filter(models.Sales.date <= endDate)

    data = query.all()
    print (data)
    if span == spanType.day:
        labels = [el["date"] for el in data]
        dataset = [el["total_sales"] for el in data]
        salesCount = [el["sales_count"] for el in data]
        totalUnits = [el["total_units"] for el in data]
    elif span == spanType.month:
        labels = [str(el["year"]) +"-"+ str(el["month"]) for el in data]
        dataset = [el["total_sales"] for el in data]
        salesCount = [el["sales_count"] for el in data]
        totalUnits = [el["total_units"] for el in data]
    else:
        labels = [el["year"] for el in data]
        dataset = [el["total_sales"] for el in data]
        salesCount = [el["sales_count"] for el in data]
        totalUnits = [el["total_units"] for el in data]
    
    return {"labels": labels, "dataset":dataset, "totalSalesCount": sum(salesCount), "totalUnits" : sum(totalUnits), "totalRevenue": sum(dataset)}

#methods

def makeRandomSales():
    randomInvoiceCount = random.randint(3,10)
    for x in range(0,randomInvoiceCount):
        salesList = []
        randomCustomer = random.choice(customersNames)
        randomSalesCount = random.randint(5, 15)
        for y in range(0, randomSalesCount):
            randomProduct = random.choice(productNames)
            randomQuantity = random.randint(1,6)
            salesList.append(
                schemas.Sale(product_name=randomProduct, quantity = randomQuantity)
            )
        randomTransaction = random.choice(["Online","InShop"])
        randomDate = random.randint(1,30)
        randomMonth = random.choice([1,2,3,4,5,6,7,8,9,10,11,12])
        randomYear = random.choice(['2022','2023'])
        randomDate = randomYear + '-'+ str(randomMonth) + '-' + str(randomDate)
        randomDateStamp = datetime.strptime(randomDate, '%Y-%m-%d')
        invoicesList.append(schemas.Receipt(customer_name = randomCustomer, 
                            transaction_type= randomTransaction,
                            date= randomDateStamp,
                            sales = salesList.copy()))

def dumpRandomsales(db:db_dependency):
    for invoice in invoicesList:
        CalculatePrice(invoice.sales, db)
        if invoice.date == None:
            invoice.date = datetime.strptime(str(datetime.today().date()), '%Y-%m-%d')
        TotalAmount = sum(x.total_price for x in invoice.sales)
        customerId = db.query(models.Customer.id).filter(models.Customer.name == invoice.customer_name).scalar()
        invoiceObj = models.Invoice(customer_id= customerId, transaction_type= invoice.transaction_type, amount= TotalAmount, date= invoice.date)
        db.add(invoiceObj)
        db.commit()
        for sale in invoice.sales:
            db.add(models.Sales(quantity=sale.quantity, total_price = sale.total_price, date = invoice.date, product_id = sale.product_id, invoice_id = invoiceObj.id))
            global total_sales
            total_sales = total_sales + 1
        db.commit()

def CalculatePrice(objs: List[schemas.Sale], db:db_dependency):
    try:
        for obj in objs:    
            obj.product_id, price = db.query(models.Product.id,models.Product.price ).filter_by(name = obj.product_name).first()
            obj.total_price = price * obj.quantity
    except Exception as e:
        print(e)
        traceback.print_exc()