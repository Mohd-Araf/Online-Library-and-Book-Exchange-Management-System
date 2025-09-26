from django.contrib import admin
from .models import OfferedBook, RequestedBook, ExchangeRequest

@admin.register(OfferedBook)
class OfferedBookAdmin(admin.ModelAdmin):
    list_display = ("title", "base_price")

@admin.register(RequestedBook)
class RequestedBookAdmin(admin.ModelAdmin):
    list_display = ("title", "base_price")

@admin.register(ExchangeRequest)
class ExchangeRequestAdmin(admin.ModelAdmin):
    list_display = ("offered_book", "requested_book", "calculated_price", "final_payment")
