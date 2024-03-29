from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('populate', views.populateAndIndex),
    path('chollos', views.getAllChollos),
    path('filter-category', views.filterByCategory),
    path('filter-price', views.filterByPrice),
    path('group-by-seller', views.chollosGroupBySource),
    path('fav-categories', views.favCategories),
    path('group-by-fav-categories', views.chollosGroupByFavCat),

]