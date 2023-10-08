# AdminDashboard_BE

It is the backend for ***Admin Dashboard*** project built in FastAPI.
It uses a relational databse i.e. MySQL as database, SQLAlchemy as an ORM

After cloning the project:
Install project dependencies using pip: `pip install -r requirements.txt`.
Start the server: `uvicorn main:app --reload`.

Access the Swagger documentation at: `http://127.0.0.1:8000/docs`.

***Project Structure***

+ *main.py*: The entry point of the application, defining routes for different modules.

Before interacting with the end points, the first and the foremost step is to hit the very first `Dump Inventory` end point to inject dummmy data in the database.

*main.py* file is the starting point and it defines further routes for different modules and these modules can be found in **Routes** directory inside project.

Each module has the relevant end points to create or read data.

**Categories**, **Products**, **Customers** has straight forward end points that are self explanatory.

**Sales** 
-> Has `Dump Sales` end point, it inserts sales with random products, random quantity and random dates.
-> Has different apis to retrieve sales for different analysis. 
-> `Sales by filter` api responds with the sales considering the filters. You can retrieve the revenue, units_sold, sales_count and sales data by giving end or start date range or applying the filter upon any product or category.

**Inventory**
-> Has `Dump Inventory` end point that injects inventory insights for random product from the databse with random dates and stocks.
-> `Inventory` end point reveals the total stock quantity for each available product and additionally it also returns the list of products that are on low stock (i.e. less than 10).
-> `Inventory Insights` end point reveals the insights of when which product's stock was injected.







