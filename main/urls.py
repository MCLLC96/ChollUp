from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAllChollos),
    path('filter-category', views.filterByCategory),
    path('filter-price', views.filterByPrice),
    path('group-by-seller', views.chollosGroupBySource),

    

]