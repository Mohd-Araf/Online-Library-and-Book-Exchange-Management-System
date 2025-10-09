from django import forms
from .models import ExchangeRequest, OfferedBook, RequestedBook

class ExchangeRequestForm(forms.ModelForm):
    class Meta:
        model = ExchangeRequest
        fields = [
            'offered_book',
            'requested_book',
            'pages_missing',
            'edition_difference',
            'condition',
            'font_side_picture',
            'back_side_picture',
            'full_book_picture',
            'author_page_picture',
        ]

    offered_book = forms.ModelChoiceField(
        queryset=OfferedBook.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select-search'})
    )
    requested_book = forms.ModelChoiceField(
        queryset=RequestedBook.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select-search'})
    )
    pages_missing = forms.IntegerField(min_value=0, initial=0, label="Pages Missing")
    edition_difference = forms.IntegerField(min_value=0, initial=0, label="Edition Difference")

    condition = forms.ChoiceField(
        choices=ExchangeRequest.CONDITION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    font_side_picture = forms.ImageField(required=True, label="Front Side Picture")
    back_side_picture = forms.ImageField(required=True, label="Back Side Picture")
    full_book_picture = forms.ImageField(required=True, label="Full Book Picture")
    author_page_picture = forms.ImageField(required=True, label="Author Page Picture")