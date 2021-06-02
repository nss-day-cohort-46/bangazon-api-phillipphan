from django.urls import path
from .views import userfavorite_list, incompleteorder_list

urlpatterns = [
    path('reports/userfavorites', userfavorite_list),
    path('reports/incompleteorders', incompleteorder_list),
]