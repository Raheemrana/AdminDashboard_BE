from typing import List
import schemas
import models


categoriesData: List[schemas.Category] = [
    schemas.Category(name="Bakery"),
    schemas.Category(name="Books and Magazines"),
    schemas.Category(name="Electronics"),
    schemas.Category(name="Sports"),
    schemas.Category(name="Gadgets"),
    schemas.Category(name="Clothing and Apparel")
]

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

customersData : List[schemas.Customer] = [
    schemas.Customer(name= "Shastri", age= 27, gender= models.Gender.Male),
    schemas.Customer(name= "Arjun", age= 27, gender= models.Gender.Male),
    schemas.Customer(name= "Miley", age= 23, gender= models.Gender.Female),
    schemas.Customer(name= "Arnold", age= 52, gender= models.Gender.Male),
    schemas.Customer(name= "Kanya", age= 22, gender= models.Gender.Male),
    schemas.Customer(name= "Hadid", age= 24, gender= models.Gender.Female),
    schemas.Customer(name= "Hanabel", age= 30, gender= models.Gender.Male),
    schemas.Customer(name= "Taylor", age= 31, gender= models.Gender.Female),
    schemas.Customer(name= "Niki", age= 42, gender= models.Gender.Female),
    schemas.Customer(name= "Kylie", age= 35, gender= models.Gender.Female),
]

