from django import forms
from .models import ExchangeRequest, OfferedBook, RequestedBook

class ExchangeRequestForm(forms.ModelForm):
    class Meta:
        model = ExchangeRequest
        fields = [
            'offered_book',
            'requested_book',
            'pages_missing',
            'condition',
            'font_side_picture',
            'back_side_picture',
            'full_book_picture',
            'author_page_picture',
        ]

    offered_book = forms.ModelChoiceField(
        queryset=OfferedBook.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select-search'}),
        label="Select Offered Book"
    )
    requested_book = forms.ModelChoiceField(
        queryset=RequestedBook.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select-search'}),
        label="Select Requested Book"
    )
    pages_missing = forms.IntegerField(
        min_value=0,
        initial=0,
        label="Pages Missing",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    condition = forms.ChoiceField(
        choices=ExchangeRequest.CONDITION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Condition"
    )

    font_side_picture = forms.ImageField(
        required=True,
        label="Front Side Picture",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    back_side_picture = forms.ImageField(
        required=True,
        label="Back Side Picture",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    full_book_picture = forms.ImageField(
        required=True,
        label="Full Book Picture",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    author_page_picture = forms.ImageField(
        required=True,
        label="Author Page Picture",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    def save(self, commit=True, user=None):
        """
        Override save method to assign the user and auto-calculate edition_difference
        """
        exchange = super().save(commit=False)
        if user:
            exchange.user = user
        # edition_difference is auto-calculated in model's save()
        if commit:
            exchange.save()
        return exchange
