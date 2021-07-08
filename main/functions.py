from main.models import Chollo, Category, Seller, Profile
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
from django.contrib.auth.models import User

from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.qparser import QueryParser
from whoosh.query import NumericRange
import os, shutil
from random import randrange

def deleteTables():
    Category.objects.all().delete()
    Chollo.objects.all().delete()
    Seller.objects.all().delete()
    Profile.objects.all().delete()


def createTables():
    print("Loading chollos and categories...")
    chollos = []

    # Obtenemos los productos de las 3 primeras páginas
    for page in range(1, 15):
        r1 = Request('https://www.chollometro.com/nuevos?page=' +
                     str(page), headers={'User-Agent': 'Mozilla/5.0'})
        base1 = urlopen(r1).read()
        s1 = BeautifulSoup(base1, "lxml")

        # Obtenemos todos los artículos de la página filtrados mediante la etiqueta id (ya que no todos son artículos) y disponibilidad
        articles = s1.find_all('article', id= True, class_= re.compile(r'(?!thread--deal|thread--expired)'))

        for a in articles:
            try:
                # Solo agregamos los chollos que tienen precio 
                price = a.find('span', class_= 'thread-price')
                if price != None and (re.compile(r'(^-)|(%$)') not in price):

                    # Conseguimos el link del chollo para obtener los datos
                    link = a.find('strong', class_='thread-title').a['href']
                    r2 = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
                    base2 = urlopen(r2).read()
                    s2 = BeautifulSoup(base2, "lxml")

                    title = s2.find('h1').string.strip()

                    price = s2.find('span', class_='thread-price').string.strip()
                    if price == 'GRATIS':
                        price = float(0.0)
                    else:
                        price = float(price.replace(
                            '€', '').replace(',', '.'))

                    description = s2.find('div', class_='cept-description-container')
                    if description != None:
                        description = '. '.join(s2.find('div', class_='cept-description-container').stripped_strings)
                    
                    category_name = s2.find('ul', class_= 'cept-breadcrumbsList').find_all('li', class_='cept-breadcrumbsList-item')[1].get_text()
                    
                    source_link = s2.find('a', class_='cept-dealBtn')['href']

                    seller_name = s2.find('h1', class_='thread-title').find_next_sibling('span').a.span.span.get_text()
                    
                    image = a.find('img')['src']

                    seller = Seller.objects.get_or_create(name= seller_name)

                    category = Category.objects.get_or_create(name= category_name)
                    
                    chollo = Chollo(title= title, price= price, description= description,
                                        category= Category.objects.get(name= category_name), source_link= source_link, seller= Seller.objects.get(name= seller_name), image= image)
                    chollos.append(chollo)

            except:
                pass

    Chollo.objects.bulk_create(chollos)


    print("Chollos inserted: " + str(Chollo.objects.count()))
    print("Categories inserted: " + str(Category.objects.count()))
    print("Finished database population")
    print("---------------------------------------------------------")

def getRandomCategories():
    categories = Category.objects.all()
    rand = randrange(categories.count())
    return categories[rand]


def createIndex():
    schema = Schema(title= TEXT(stored=True), price=NUMERIC(numtype=float, stored=True), category=TEXT(stored=True), description=TEXT(stored=True), source_link=TEXT(stored=True), seller=TEXT(stored=True), image=TEXT(stored=True))

    # Eliminamos el directorio del í­ndice, si existe
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")

    #Creamos el í­ndice
    ix = create_in("Index", schema=schema)

    # Creamos un writer para poder añadir documentos al indice
    writer = ix.writer()
    i= 0
    chollos = Chollo.objects.all()
    for c in chollos:
        # Añade cada chollo de la lista al índice
        writer.add_document(title= c.title, price= c.price, category= c.category.name, description= c.description, source_link= c.source_link, seller= c.seller.name, image= c.image)    
        i+=1
    writer.commit()
    print('Fin de indexado. Se han indexado '+ str(i) + ' chollos')


def searchByCategory(category_name):
    ix=open_dir("Index")
    chollos = []

    with ix.searcher() as searcher:
        query = QueryParser("category", ix.schema).parse(category_name)
        results = searcher.search(query)
        
        #Importante: el diccionario solo contiene los campos que han sido almacenados(stored=True) en el Schema
        for r in results:
            chollos.append(Chollo(title= r['title'], price= r['price'], category= Category(name= r['category']), description= r['description'], source_link= r['source_link'], seller= Seller(name= r['seller']), image= r['image'])) 
       
    return chollos

def searchByPrice(min_price, max_price):
    ix=open_dir("Index")
    chollos = []

    with ix.searcher() as searcher:
        query = NumericRange('price', min_price, max_price)
        results = searcher.search(query)

        for r in results:
            chollos.append(Chollo(title= r['title'], price= r['price'], category= Category(name= r['category']), description= r['description'], source_link= r['source_link'], seller= Seller(name= r['seller']), image= r['image'])) 

    return chollos

# if __name__ == '__main__':
    # populateDatabase()
