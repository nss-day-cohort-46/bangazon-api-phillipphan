import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection

def completeorder_list(request):
    if request.method == "GET":
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
                SELECT
                    o.id,
                    u.first_name || ' ' || u.last_name AS full_name,
                    pay.merchant_name,
                    SUM(p.price) AS total
                FROM
                    bangazonapi_order  o
                JOIN
                    bangazonapi_customer c ON c.id = o.customer_id
                JOIN
                    auth_user u ON u.id = c.user_id
                JOIN
                    bangazonapi_orderproduct op ON op.order_id = o.id
                JOIN
                    bangazonapi_product p ON p.id = op.product_id
                JOIN
                    bangazonapi_payment pay ON pay.id = o.payment_type_id
                WHERE
                    payment_type_id IS NOT NULL
                GROUP BY
                    o.id
            """)

            dataset = db_cursor.fetchall()

            complete_orders = {}

            for row in dataset:
                uid = row["id"]

                complete_orders[uid] = {}
                complete_orders[uid]["id"] = uid
                complete_orders[uid]["total"] = row["total"]
                complete_orders[uid]["full_name"] = row["full_name"]
                complete_orders[uid]["merchant_name"] = row["merchant_name"]

            
    list_of_complete_orders = complete_orders.values()

    template = "orders/list_with_complete_orders.html"
    context = {
        "completeorders_list": list_of_complete_orders
    }

    return render(request, template, context)