# AdminDashboard_BE

It is the backend for ***Admin Dashboard*** project built in FastAPI.  
It uses a relational database i.e. MySQL as database, SQLAlchemy as an ORM

After cloning the project:
Install project dependencies using pip: `pip install -r requirements.txt`.<br>
Start the server: `uvicorn main:app --reload`.

Access the Swagger documentation at: `http://127.0.0.1:8000/docs`.  

## ***Before You Begin***

Make sure to set up MySQL and update the DB url in `database.py`

Before interacting with any endpoints, ensure to hit the `Dump Inventory` endpoint first. This step injects dummy data consisting of categories, products, customers and sales into the database, allowing you to interact with other endpoints effectively.  

## ***Project Structure***

+ *main.py*: The entry point of the application, defining routes for different modules.
+ Each module has the relevant end points to create or read data.
+ *Routes/*: Directory containing modules with specific endpoints.
  + Categories: Manages product categories.
  + Products: Handles product-related endpoints.
  + Customers: Manages customer-related operations.
  + Sales:  
    `Dump Sales` Inserts sales data with random products, quantities, and dates.<br>
    `Sales Analysis` Provides various APIs for sales analysis, including filtering by date range, product, or category.
  + Inventory:  
    `Dump Inventory` Injects inventory data for random products with dates and stock quantities.<br>
    `Inventory` Retrieves total stock quantity for each product and identifies products with low stock (less than 10 units).<br>
    `Inventory Insights` Provides insights into stock injection history for products.  

Feel free to explore and analyze sales data, manage product inventory, and gain valuable insights for better decision-making!

Happy coding! 🚀





