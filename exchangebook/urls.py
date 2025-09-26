from django.urls import path
from . import views
app_name = "exchangebook"

urlpatterns = [
    path("search/", views.search_books, name="search"),
    path("exchange/", views.exchange_book, name="exchange"),
]