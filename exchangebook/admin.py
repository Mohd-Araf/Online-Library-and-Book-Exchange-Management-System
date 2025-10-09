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
    list_display = ("title", "user", "base_price", "edition")
    list_editable = ("base_price", "edition")
    list_filter = ("user", "edition")
    search_fields = ("title", "user__username")


@admin.register(ExchangeRequest)
class ExchangeRequestAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "offered_book",
        "requested_book",
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
    readonly_fields = ("edition_difference",)  # auto-calculated

    # Auto assign user and calculate edition_difference
    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user  # current admin auto-assigned
        # auto calculate edition_difference
        if obj.offered_book and obj.requested_book:
            obj.edition_difference = abs(obj.offered_book.edition - obj.requested_book.edition)
        super().save_model(request, obj, form, change)
