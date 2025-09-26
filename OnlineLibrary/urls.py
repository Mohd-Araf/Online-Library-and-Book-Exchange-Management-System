from django.contrib import admin

from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from users.views import CustomLoginView, ResetPasswordView, ChangePasswordView
from users.views import profile
from users.forms import LoginForm
from django.contrib import admin
from django.urls import path
from django.shortcuts import render   # render import করতে হবে

# Simple view function (app ছাড়াই rules.html দেখানোর জন্য)
def rules_view(request):
    return render(request, 'rules.html')




urlpatterns = [
    path('contactus/', contact_view,name='contact'),
    path('rules/', rules_view, name='rules'),
    path('admin/', admin.site.urls),
path('rules/', rules_view, name='rules'),
    path('', include('users.urls')),
    path('', include('sell_books.urls')),
    path('exchange/', include('exchangebook.urls')),

    path('accounts/', include('django.contrib.auth.urls')),

    path('profile/', profile, name='users-profile'),

 path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html',
                                           authentication_form=LoginForm), name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('password-change/', ChangePasswordView.as_view(), name='password_change'),

    re_path(r'^oauth/', include('social_django.urls', namespace='social')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
