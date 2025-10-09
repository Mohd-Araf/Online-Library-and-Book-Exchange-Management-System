from django.db import models

class OfferedBook(models.Model):
    title = models.CharField(max_length=200)
    base_price = models.PositiveIntegerField()
    edition = models.PositiveIntegerField(default=1)
    total_pages = models.PositiveIntegerField(default=100)  # Admin set-able

    def __str__(self):
        return f"{self.title} (Base: {self.base_price})"


class RequestedBook(models.Model):
    title = models.CharField(max_length=200)
    base_price = models.PositiveIntegerField()
    edition = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} (Base: {self.base_price})"


class ExchangeRequest(models.Model):
    offered_book = models.ForeignKey(OfferedBook, on_delete=models.CASCADE)
    requested_book = models.ForeignKey(RequestedBook, on_delete=models.CASCADE)

    pages_missing = models.PositiveIntegerField()
    edition_difference = models.PositiveIntegerField()

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

    def calculate_edition_difference(self):
        offered_edition = self.offered_book.edition or 1
        requested_edition = self.requested_book.edition or 1
        return abs(offered_edition - requested_edition)

    def __str__(self):
        return f"Exchange {self.offered_book.title} → {self.requested_book.title}"