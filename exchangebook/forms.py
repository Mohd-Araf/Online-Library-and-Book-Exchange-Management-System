from django import forms
from .models import ExchangeRequest, OfferedBook, RequestedBook

class ExchangeRequestForm(forms.ModelForm):
    class Meta:
        model = ExchangeRequest
        fields = ['offered_book', 'requested_book', 'pages_missing', 'edition_difference', 'condition']

    offered_book = forms.ModelChoiceField(
        queryset=OfferedBook.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select-search'})
    )
    requested_book = forms.ModelChoiceField(
        queryset=RequestedBook.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select-search'})

    )
    pages_missing = forms.IntegerField(min_value=0, initial=0)
    edition_difference = forms.IntegerField(min_value=0, initial=0)
    condition = forms.ChoiceField(
        choices=ExchangeRequest.CONDITION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
