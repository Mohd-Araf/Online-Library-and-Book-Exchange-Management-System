from django.contrib import admin
from .models import OfferedBook, RequestedBook, ExchangeRequest

@admin.register(OfferedBook)
class OfferedBookAdmin(admin.ModelAdmin):
    list_display = ("title", "base_price", "edition", "total_pages")
    list_editable = ("base_price", "edition", "total_pages")


@admin.register(RequestedBook)
class RequestedBookAdmin(admin.ModelAdmin):
    list_display = ("title", "base_price", "edition")
    list_editable = ("base_price", "edition")


@admin.register(ExchangeRequest)
class ExchangeRequestAdmin(admin.ModelAdmin):
    list_display = (
        "offered_book",
        "requested_book",
        "pages_missing",
        "edition_difference",
        "condition",
        "calculated_price",
        "final_payment"
    )