from main.models import Chollo, Category, Seller
from urllib.request import Request, urlopen
import re
from django.contrib.auth.models import User

import os, shutil
from random import randrange

def deleteTables():
    Category.objects.all().delete()
    Chollo.objects.all().delete()
    Seller.objects.all().delete()


def createTables():
    print("Loading chollos and categories...")
    chollos = []

    # Obtenemos los productos de las 3 primeras páginas
    

def getRandomCategories():
    categories = Category.objects.all()
    rand = randrange(categories.count())
    return categories[rand]

def searchByCategory(category):
    chollos = []

    chollos=list(Chollo.objects.filter(category=category))
    return chollos

def searchByPrice(min,max):
    chollosIn = []

    chollos=list(Chollo.objects.all())
    for chollo in chollos:
        if chollo.price < max and chollo.price > min:
            chollosIn.append(chollo)
    return chollosIn






# if __name__ == '__main__':
    # populateDatabase()
