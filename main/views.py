from django.http import HttpResponse
from django.shortcuts import render
from main.functions import deleteTables, createTables, searchByCategory, searchByPrice
from main.models import Chollo, Category
from main.forms import FormPrice, FormCategory, FormFavCategory
from django.contrib.auth.models import User
from django.shortcuts import redirect
import shelve

import json
from django.views.decorators.csrf import csrf_exempt

def getAllChollos(request):
    chollos = Chollo.objects.all()
    alert = True
    if chollos.count() != 0:
        alert = False

    return render(request, 'chollos.html', {'chollos': chollos, 'alert': alert})
    


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
        pass
        
        form_cat = FormCategory(request.POST)
        if form_cat.is_valid():
            category = form_cat.cleaned_data['category']
            chollos = searchByCategory(category)
        
    else:
        form_cat= FormCategory()

    return render(request, 'searchByCategory.html', {'chollos': chollos,'form_cat': form_cat, 'populate': isPopulated()})

@csrf_exempt
def filterByPrice(request):
    chollos = None
    
    if request.method == 'POST':
        pass
        
        form_price = FormPrice(request.POST)

        if form_price.is_valid():
            min_price = form_price.cleaned_data['min_price']
            max_price = form_price.cleaned_data['max_price']
            chollos = searchByPrice(min_price, max_price)
        
    else:  
        form_price=FormPrice()

    return render(request, 'searchByPrice.html', {'chollos': chollos,'form_price': form_price, 'populate': isPopulated()})


