from django.http import HttpResponse
from django.shortcuts import render
from main.functions import deleteTables, createTables, createIndex, searchByCategory, searchByPrice
from main.models import Chollo, Profile, Category
from main.forms import FormPrice, FormCategory, FormFavCategory
from django.contrib.auth.models import User
from django.shortcuts import redirect
import shelve

import json
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')

def getAllChollos(request):
    chollos = Chollo.objects.all()
    alert = True
    if chollos.count() != 0:
        alert = False

    return render(request, 'chollos.html', {'chollos': chollos, 'alert': alert})
    
    
def populateAndIndex(request):
    if request.user.is_superuser:
        deleteTables()
        createTables()
        createIndex()
        return redirect('/chollos')
    else:
        return render(request, 'index.html', {'alert': True})

@csrf_exempt
def favCategories(request):
    if request.user.is_authenticated:
        n_categories = Category.objects.all().count()
        if n_categories > 0:
            if request.user.is_authenticated:
                user_id = request.user.pk
                profile = Profile.objects.get_or_create(user_id= user_id)[0]
                
                if request.method == 'POST':
                    form_fav_cat = FormFavCategory(request.POST)
                    
                    if form_fav_cat.is_valid():
                        categories = form_fav_cat.cleaned_data['categories']
                        profile.favourite_categories.clear()

                        for c in categories:
                            profile.favourite_categories.add(c)
                        profile.save()
                        alert = True    
                else:
                    categories = profile.favourite_categories.all()
                    form_fav_cat = FormFavCategory(initial={'categories': categories})
                    alert = False

                return render(request, 'favCategories.html', {'form_fav_cat': form_fav_cat, 'cat': n_categories, 'alert': alert})
        
        else:
            return render(request, 'favCategories.html', {'msj': 'Aún no se han proporcionado datos al sistema.', 'cat': n_categories})
    else:
        return render(request, 'favCategories.html', {'msj': 'El usuario debe iniciar sesión.'})

def chollosGroupBySource(request):
    chollos = Chollo.objects.all().order_by('seller')
    return render(request,'chollosBySeller.html', {'chollos': chollos})

def isPopulated():
    res = False
    if Chollo.objects.all().count() > 0:
        res = True
    return res

@csrf_exempt    
def filterByCategory(request):
    chollos = None

    if request.method == 'POST':
        form_cat = FormCategory(request.POST)

        if form_cat.is_valid():
            category = form_cat.cleaned_data['category']
            chollos = searchByCategory(category.name)
    else:
        form_cat= FormCategory()

    return render(request, 'searchByCategory.html', {'chollos': chollos,'form_cat': form_cat, 'populate': isPopulated()})

@csrf_exempt
def filterByPrice(request):
    chollos = None
    
    if request.method == 'POST':
        form_price = FormPrice(request.POST)

        if form_price.is_valid():
            min_price = form_price.cleaned_data['min_price']
            max_price = form_price.cleaned_data['max_price']
            chollos = searchByPrice(min_price, max_price)
    else:  
        form_price=FormPrice()

    return render(request, 'searchByPrice.html', {'chollos': chollos,'form_price': form_price, 'populate': isPopulated()})


def chollosGroupByFavCat(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get_or_create(user_id= request.user.pk)[0]
        if profile != None:
            fav_categories = profile.favourite_categories.all()
            if fav_categories.count() > 0:
                chollos = Chollo.objects.filter(category__in= fav_categories).order_by('category')
                
                return render(request,'chollosByFavCategory.html', {'chollos': chollos, 'fc': fav_categories.count()})

            else:
                return render(request,'chollosByFavCategory.html', {'msj': 'El usuario no tiene asignada ninguna categoría favorita.'})

    else:
        return render(request,'chollosByFavCategory.html', {'msj': 'El usuario debe iniciar sesión.'})