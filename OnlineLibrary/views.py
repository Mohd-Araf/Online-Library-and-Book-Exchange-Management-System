
from django.shortcuts import render


def rules_view(request):
    return render(request, 'rules.html')
def contact_view(request):
    return render(request, 'contactus.html')