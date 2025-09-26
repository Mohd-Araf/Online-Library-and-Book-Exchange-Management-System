from django.shortcuts import render, get_object_or_404, redirect
from .models import SellBook

def sell_book_list(request):
    query = request.GET.get('q')
    if query:
        books = SellBook.objects.filter(name__icontains=query) | SellBook.objects.filter(author__icontains=query)
    else:
        books = SellBook.objects.all()
    return render(request, 'sellbooks/booklist.html', {'books': books})

def buy_book_view(request, book_id):
    book = get_object_or_404(SellBook, id=book_id)
    if request.method == 'POST':

        return redirect('buy-success', buy_id=book.id)
    return render(request, 'sellbooks/sellbooks.html', {'book': book})


def buy_success_view(request, buy_id):
    book = get_object_or_404(SellBook, id=buy_id)
    return render(request, 'sellbooks/success.html', {'book': book})
