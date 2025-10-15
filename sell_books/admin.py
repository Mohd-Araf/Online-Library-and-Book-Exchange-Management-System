from django.contrib import admin
from .models import BookType, SellBook

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
