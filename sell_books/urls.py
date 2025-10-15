from django.urls import path
from . import views

urlpatterns = [
    path('sell/books/', views.sell_book_list, name='sell-book-list'),
    path('sell/buy/<int:book_id>/', views.buy_book_view, name='buy-book'),
]
