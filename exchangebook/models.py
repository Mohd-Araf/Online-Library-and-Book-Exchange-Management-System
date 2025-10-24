from django.db import models
from django.contrib.auth.models import User

class OfferedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offered_books")  # Owner
    title = models.CharField(max_length=200)
    base_price = models.PositiveIntegerField()
    edition = models.PositiveIntegerField(default=1)
    total_pages = models.PositiveIntegerField(default=100)

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
    edition_difference = models.IntegerField(null=True, blank=True)
    calculated_price = models.IntegerField(null=True, blank=True)
    final_payment = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        offered_edition = self.offered_book.edition or 1
        user_edition = self.user_edition or 1
        self.edition_difference = offered_edition - user_edition

        base_price = self.offered_book.base_price
        offered_price = base_price * 0.6  # starting value

        offered_price -= (base_price * 0.05 * abs(self.edition_difference))

        total_pages = self.offered_book.total_pages or 100
        missing_percent = (self.pages_missing / total_pages) * 100
        offered_price -= (base_price * 0.005 * missing_percent)

        condition_adjustment = {
            "excellent": 0.01,
            "fine": 0.03,
            "not_good": 0.05
        }
        offered_price -= base_price * condition_adjustment.get(self.condition, 0)

        if offered_price < 0:
            offered_price = 0

        self.calculated_price = int(offered_price)

        requested_price = getattr(self.requested_book, "price", 0)
        self.final_payment = int(requested_price - offered_price)

        super().save(*args, **kwargs)

    @property
    def final_payment_for_display(self):
        return abs(self.final_payment) if self.final_payment is not None else 0

    def __str__(self):
        return f"Exchange {self.offered_book.title} → {self.requested_book.title}"
