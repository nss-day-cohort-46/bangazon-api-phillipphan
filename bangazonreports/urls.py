from django.urls import path
from .views import userfavorite_list

urlpatterns = [
    path('reports/userfavorites', userfavorite_list),
]