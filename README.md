# AdminDashboard_BE

It is the backend for ## Admin Dashboard project built in FastAPI.
It uses a relational databse i.e. MySQL as database, SQLAlchemy as an ORM

In order to run this project try running `pip install -r requirements.txt` command in your cmd.
After intalling dependencies you can run the server with `uvicorn main:app --reload` command.

You can open the swagger docs at this url `http://127.0.0.1:8000/docs`

Before interacting with the end points, the first and the foremost step is to hit the very first `Dump Inventory` end point to inject dummmy data in the project.

The ### main.py file is the starting point and it defines further routes for different sections and these sections can be found in ###Routes directory inside project.

Each section has the relevant end point to create or read data. 

'Sales' section has `Dump Sales` end point, it inserts random sales with random products, random quantity and random dates.

