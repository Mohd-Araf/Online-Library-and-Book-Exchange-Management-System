from django.db import models
from django.contrib.auth.models import User
from sell_books.models import SellBook
from exchangebook.models import ExchangeRequest  # assuming you have ExchangeRequest model

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    sell_book = models.ForeignKey(SellBook, on_delete=models.SET_NULL, null=True, blank=True)
    exchange_request = models.ForeignKey(ExchangeRequest, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_id} ({self.status})"
