from django import forms
from .models import Category
from django.forms import ModelChoiceField, ModelMultipleChoiceField

class FormPrice(forms.Form):
    min_price = forms.FloatField(label='Precio mínimo',widget= forms.NumberInput(attrs={'class':'has-popover form-control rounded-pill border-0 shadow-sm px-4 mb-3', 'data-content':'Añada un precio mínimo', 'data-placement':'right', 'data-container':'body'}), min_value= 0.0)
    max_price = forms.FloatField(label='Precio máximo',widget= forms.NumberInput(attrs={'class':'has-popover form-control rounded-pill border-0 shadow-sm px-4', 'data-content':'Añada un precio máximo', 'data-placement':'right', 'data-container':'body'}), min_value= 0.0)

class FormCategory(forms.Form):
    category = ModelChoiceField(label='Categoría',widget= forms.Select(attrs={'class':'has-popover form-control rounded-pill border-0 shadow-sm px-4', 'data-content':'Seleccione una categoría', 'data-placement':'right', 'data-container':'body'}), queryset= Category.objects.all())

class FormFavCategory(forms.Form):
    categories = ModelMultipleChoiceField(label='Selecciona las categorías', widget= forms.CheckboxSelectMultiple(attrs={'data-container':'body'}), queryset= Category.objects.all(), required= False)