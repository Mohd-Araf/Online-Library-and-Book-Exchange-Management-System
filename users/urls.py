from django.urls import path
from . import views
from .views import home, profile, RegisterView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
]
