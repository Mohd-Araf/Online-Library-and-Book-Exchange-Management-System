from django.db import models
from django.contrib.auth.models import User  # Import User model

class OfferedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offered_books")  # Owner
    title = models.CharField(max_length=200)
    base_price = models.PositiveIntegerField()
    edition = models.PositiveIntegerField(default=1)
    total_pages = models.PositiveIntegerField(default=100)  # Admin set-able

    def __str__(self):
        return f"{self.title} (Base: {self.base_price})"

class RequestedBook(models.Model):
    title = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    exchangeable_amount = models.PositiveIntegerField(default=0)

    def final_amount(self):
        return self.price - self.exchangeable_amount

    def __str__(self):
        return f"{self.title} (Price: {self.price})"

class ExchangeRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exchange_requests")
    offered_book = models.ForeignKey(OfferedBook, on_delete=models.CASCADE)
    requested_book = models.ForeignKey(RequestedBook, on_delete=models.CASCADE)

    user_edition = models.PositiveIntegerField(default=1)
    pages_missing = models.PositiveIntegerField(default=0)
    condition_choices = [
        ('excellent', 'Excellent'),
        ('fine', 'Fine'),
        ('not_good', 'Not Good'),
    ]
    condition = models.CharField(max_length=20, choices=condition_choices, default='excellent')

    front_side_picture = models.ImageField(upload_to="exchange_books/", default="exchange_books/default.jpg")
    back_side_picture = models.ImageField(upload_to="exchange_books/", default="exchange_books/default.jpg")
    full_book_picture = models.ImageField(upload_to="exchange_books/", default="exchange_books/default.jpg")
    author_page_picture = models.ImageField(upload_to="exchange_books/", default="exchange_books/default.jpg")

    # Calculated fields
    edition_difference = models.IntegerField(null=True, blank=True)
    calculated_price = models.IntegerField(null=True, blank=True)
    final_payment = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Edition difference
        self.edition_difference = self.offered_book.edition - self.user_edition

        # Adjustment based on edition difference
        adjustment = self.edition_difference * 100  # Example: each edition difference = 100 unit adjustment

        # Condition multiplier
        condition_multiplier = {
            'excellent': 1.0,
            'fine': 0.9,
            'not_good': 0.7
        }

        # Calculated price
        self.calculated_price = int(self.offered_book.base_price * condition_multiplier[self.condition] - adjustment)

        # Final payment (can be negative)
        self.final_payment = self.requested_book.final_amount() - self.calculated_price

        super().save(*args, **kwargs)

    @property
    def final_payment_for_display(self):
        """Always positive value for display in template"""
        if self.final_payment < 0:
            return abs(self.final_payment)
        return 0

    def __str__(self):
        return f"Exchange {self.offered_book.title} → {self.requested_book.title}"
