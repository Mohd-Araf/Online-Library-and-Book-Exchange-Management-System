from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required

from exchangebook.models import ExchangeRequest
from sell_books.models import SellBook, PurchasedBook
from payment.models import Payment
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm

def home(request):
    return render(request, 'users/index.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect(to='login')
        return render(request, self.template_name, {'form': form})

class CustomLoginView(LoginView):
    form_class = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password if an account exists with the email you entered."
    success_url = reverse_lazy('users-home')

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    user = request.user

    # Handle profile update
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=user)
        profile_form = UpdateProfileForm(instance=user.profile)

    # Fetch user's exchanges
    exchanges = ExchangeRequest.objects.filter(user=user)

    # Fetch user's purchased books (only successful payments)
    purchased_book_ids = Payment.objects.filter(user=user, status='Successful', sell_book__isnull=False)\
                                        .values_list('sell_book', flat=True)
    purchases = PurchasedBook.objects.filter(user=user, book__id__in=purchased_book_ids)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'exchanges': exchanges,
        'purchases': purchases,
    }

    return render(request, 'users/profile.html', context)
