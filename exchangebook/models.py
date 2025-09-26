from django.db import models

class OfferedBook(models.Model):
    title = models.CharField(max_length=200)
    base_price = models.PositiveIntegerField()  # admin set korbe int hisebe

    def __str__(self):
        return f"{self.title} (Base: {self.base_price})"


class RequestedBook(models.Model):
    title = models.CharField(max_length=200)
    base_price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} (Base: {self.base_price})"


class ExchangeRequest(models.Model):
    offered_book = models.ForeignKey(OfferedBook, on_delete=models.CASCADE)
    requested_book = models.ForeignKey(RequestedBook, on_delete=models.CASCADE)
    pages_missing = models.PositiveIntegerField(default=0)
    edition_difference = models.PositiveIntegerField(default=0)  # how many editions behind

    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('fine', 'Fine'),
        ('not_good', 'Not Good'),
    ]
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)

    calculated_price = models.PositiveIntegerField(null=True, blank=True)
    final_payment = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Exchange {self.offered_book.title} → {self.requested_book.title}"
