from django.urls import path
from .views import userfavorite_list, incompleteorder_list, inexpensiveproduct_list, expensiveproduct_list, completeorder_list

urlpatterns = [
    path('reports/userfavorites', userfavorite_list),
    path('reports/incompleteorders', incompleteorder_list),
    path('reports/inexpensiveproducts', inexpensiveproduct_list),
    path('reports/expensiveproducts', expensiveproduct_list),
    path('reports/completeorders', completeorder_list),
]