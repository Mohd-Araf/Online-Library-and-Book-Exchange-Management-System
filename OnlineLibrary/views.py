from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

def rules_view(request):
    return render(request, 'rules.html')


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(
                subject,
                full_message,
                email,  # From user email
                ['22201138@uap-bd.edu'],  # To your Gmail
                fail_silently=False,
            )
            messages.success(request, "Message sent successfully!")
        except Exception as e:
            messages.error(request, f"Error: {e}")

        return redirect('contact')  # Contact page er url name

    return render(request, 'contactus.html')