from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Seller(models.Model):
    name = models.CharField(max_length=30, verbose_name= 'Vendedor')

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name= 'Categoría')

    def __str__(self):
        return self.name
    
class Chollo(models.Model):
    title = models.TextField(verbose_name= 'Título')
    price  = models.FloatField(validators= [MinValueValidator(0.0)], verbose_name= 'Precio')
    description = models.TextField(verbose_name= 'Descripción')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name= 'Categoría')
    source_link = models.URLField(verbose_name= 'Link de la fuente')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, verbose_name= 'Vendedor')
    image = models.URLField(verbose_name= 'URL imagen')

    def __str__(self):
        return self.title
    
    