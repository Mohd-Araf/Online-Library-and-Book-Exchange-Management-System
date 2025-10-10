from django.shortcuts import render, get_object_or_404, redirect
from .models import SellBook, PurchasedBook
from django.contrib.auth.decorators import login_required

def sell_book_list(request):
    query = request.GET.get('q')
    if query:
        books = SellBook.objects.filter(name__icontains=query) | SellBook.objects.filter(author__icontains=query)
    else:
        books = SellBook.objects.all()
    return render(request, 'sellbooks/booklist.html', {'books': books})

@login_required
def buy_book_view(request, book_id):
    book = get_object_or_404(SellBook, id=book_id)

    if request.method == 'POST':
        # Check if the user already purchased this book
        if not PurchasedBook.objects.filter(user=request.user, book=book).exists():
            PurchasedBook.objects.create(user=request.user, book=book)

        return redirect('buy-success', buy_id=book.id)

    return render(request, 'sellbooks/sellbooks.html', {'book': book})


@login_required
def buy_success_view(request, buy_id):
    book = get_object_or_404(SellBook, id=buy_id)
    return render(request, 'sellbooks/success.html', {'book': book})
