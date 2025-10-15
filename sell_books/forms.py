from django import forms
from .models import SellBook

class SellBookForm(forms.ModelForm):
    class Meta:
        model = SellBook
        fields = ['name', 'booktype', 'author', 'price', 'image',]
        widgets = {
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }
