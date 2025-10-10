from django.contrib import admin
from .models import OfferedBook, RequestedBook, ExchangeRequest

@admin.register(OfferedBook)
class OfferedBookAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "base_price", "edition", "total_pages")
    list_editable = ("base_price", "edition", "total_pages")
    list_filter = ("user", "edition")
    search_fields = ("title", "user__username")


@admin.register(RequestedBook)
class RequestedBookAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "exchangeable_amount")
    list_editable = ("price", "exchangeable_amount")
    search_fields = ("title",)
    list_filter = ("price",)

@admin.register(ExchangeRequest)
class ExchangeRequestAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "offered_book",
        "requested_book",
        "user_edition",
        "pages_missing",
        "edition_difference",
        "condition",
        "calculated_price",
        "final_payment",
    )
    list_filter = ("condition", "user")
    search_fields = (
        "offered_book__title",
        "requested_book__title",
        "user__username",
    )