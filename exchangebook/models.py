from django.db import models
from django.contrib.auth.models import User  # Import User model

class OfferedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offered_books") # Owner
    title = models.CharField(max_length=200)
    base_price = models.PositiveIntegerField()
    edition = models.PositiveIntegerField(default=1)
    total_pages = models.PositiveIntegerField(default=100)  # Admin set-able

    def __str__(self):
        return f"{self.title} (Base: {self.base_price})"


class RequestedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exchanges")
    title = models.CharField(max_length=200)
    base_price = models.PositiveIntegerField()
    edition = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} (Base: {self.base_price})"


class ExchangeRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exchange_requests")

    offered_book = models.ForeignKey(OfferedBook, on_delete=models.CASCADE)
    requested_book = models.ForeignKey(RequestedBook, on_delete=models.CASCADE)

    pages_missing = models.PositiveIntegerField()
    edition_difference = models.PositiveIntegerField(blank=True, null=True)

    font_side_picture = models.ImageField(upload_to="exchange_books/", default="exchange_books/default.jpg")
    back_side_picture = models.ImageField(upload_to="exchange_books/", default="exchange_books/default.jpg")
    full_book_picture = models.ImageField(upload_to="exchange_books/", default="exchange_books/default.jpg")
    author_page_picture = models.ImageField(upload_to="exchange_books/", default="exchange_books/default.jpg")

    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('fine', 'Fine'),
        ('not_good', 'Not Good'),
    ]
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)

    calculated_price = models.PositiveIntegerField(null=True, blank=True)
    final_payment = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-calculate edition_difference
        self.edition_difference = abs(self.offered_book.edition - self.requested_book.edition)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Exchange {self.offered_book.title} → {self.requested_book.title}"
