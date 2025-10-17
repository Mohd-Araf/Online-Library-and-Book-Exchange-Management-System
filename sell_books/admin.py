from django.contrib import admin
from .models import BookType, SellBook, PurchasedBook


@admin.register(BookType)
class BookTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(SellBook)
class SellBookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'booktype', 'price', 'user')
    search_fields = ('name', 'author')
    list_filter = ('booktype',)
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()


@admin.register(PurchasedBook)
class PurchasedBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book_name', 'author_name', 'price')
    search_fields = ('user__username', 'book__name', 'book__author')
    list_filter = ('user',)

    def book_name(self, obj):
        return obj.book.name

    def author_name(self, obj):
        return obj.book.author

    def price(self, obj):
        return obj.book.price
