import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection

def inexpensiveproduct_list(request):
    if request.method == "GET":
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
                SELECT
                    p.id,
                    p.name,
                    p.price,
                    p.description,
                    p.location
                FROM
                    bangazonapi_product p
                WHERE
                    p.price < 999
            """)

            dataset = db_cursor.fetchall()

            inexpensive_products = {}

            for row in dataset:
                id = row["id"]

                inexpensive_products[id] = {}
                inexpensive_products[id]["id"] = id
                inexpensive_products[id]["name"] = row["name"]
                inexpensive_products[id]["price"] = row["price"]
                inexpensive_products[id]["description"] = row["description"]
                inexpensive_products[id]["location"] = row["location"]

    list_of_inexpensive_products = inexpensive_products.values()

    template = "products/list_with_inexpensive_products.html"
    context = {
        "inexpensiveproducts_list": list_of_inexpensive_products
    }

    return render(request, template, context)