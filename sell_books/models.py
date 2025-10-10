from django.db import models
from django.contrib.auth.models import User

class BookType(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class SellBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sell_books')
    name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    booktype = models.ForeignKey(BookType, on_delete=models.CASCADE)
    author = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='sell_book_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class PurchasedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_books')
    book = models.ForeignKey(SellBook, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.book.name}"
