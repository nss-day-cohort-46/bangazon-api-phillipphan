import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection

def expensiveproduct_list(request):
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
                    p.price > 999
            """)

            dataset = db_cursor.fetchall()

            expensive_products = {}

            for row in dataset:
                id = row["id"]

                expensive_products[id] = {}
                expensive_products[id]["id"] = id
                expensive_products[id]["name"] = row["name"]
                expensive_products[id]["price"] = row["price"]
                expensive_products[id]["description"] = row["description"]
                expensive_products[id]["location"] = row["location"]

    list_of_expensive_products = expensive_products.values()

    template = "products/list_with_expensive_products.html"
    context = {
        "expensiveproducts_list": list_of_expensive_products
    }

    return render(request, template, context)