from django.contrib import admin
from .models import BookType, SellBook

# ------------------------------
# BookType Admin
# ------------------------------
@admin.register(BookType)
class BookTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Columns to display in admin list view
    search_fields = ('name',)               # Add search box for BookType

# ------------------------------
# SellBook Admin
# ------------------------------
@admin.register(SellBook)
class SellBookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'booktype', 'price')  # Columns to display
    search_fields = ('name', 'author')                        # Search by name or author
    list_filter = ('booktype',)                               # Filter sidebar by book type
    readonly_fields = ()                                     # Add if any field is read-only
