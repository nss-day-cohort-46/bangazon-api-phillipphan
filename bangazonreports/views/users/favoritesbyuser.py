import sqlite3
from django.shortcuts import render
from bangazonapi.models import Customer
from bangazonreports.views import Connection

def userfavorite_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
                SELECT
                    c.id AS customer_id,
                    c.phone_number,
                    c.address,
                    u.first_name || ' ' || u.last_name AS customer_name,
                    su.first_name || ' ' || su.last_name AS seller_name
                FROM 
                    bangazonapi_customer c
                LEFT JOIN
                    bangazonapi_favorite f ON f.customer_id = c.id
                JOIN
                    auth_user u ON c.user_id = u.id
                LEFT JOIN
                    bangazonapi_customer sc ON f.seller_id = sc.id
                LEFT JOIN
                    auth_user su ON sc.user_id = su.id
            """)

            dataset = db_cursor.fetchall()

            favorites_by_user = {}

            for row in dataset:
                seller = Customer()
                seller.seller_name = row["seller_name"]
                uid = row["customer_id"]

                if uid in favorites_by_user:
                    favorites_by_user[uid]["sellers"].append(seller)

                else:
                    favorites_by_user[uid] = {}
                    favorites_by_user[uid]["id"] = uid
                    favorites_by_user[uid]["customer_name"] = row["customer_name"]
                    favorites_by_user[uid]["address"] = row["address"]
                    favorites_by_user[uid]["phone_number"] = row["phone_number"]
                    favorites_by_user[uid]["sellers"] = [seller]

        list_of_users_with_favorites = favorites_by_user.values()

        template = 'users/list_with_favorites.html'
        context = {
            'userfavorites_list': list_of_users_with_favorites
        }

        return render(request, template, context)