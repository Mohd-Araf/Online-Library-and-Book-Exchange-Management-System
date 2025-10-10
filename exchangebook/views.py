from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ExchangeRequestForm
from .models import OfferedBook, RequestedBook, ExchangeRequest

def search_books(request):
    return render(request, "exchange/search.html")


@login_required(login_url="/accounts/login/")
def exchange_book(request):
    if request.method == "POST":
        form = ExchangeRequestForm(request.POST, request.FILES)
        if form.is_valid():

            exchange = form.save(commit=False)
            exchange.user = request.user

            offered_edition = exchange.offered_book.edition or 1
            user_edition = exchange.user_edition or 1
            edition_diff = offered_edition - user_edition
            exchange.edition_difference = edition_diff

            # --- Offered Book calculated price ---
            base_price = exchange.offered_book.base_price
            offered_price = base_price * 0.6  # starting value

            # Adjust for edition difference
            offered_price -= (base_price * 0.05 * abs(edition_diff))

            # Adjust for missing pages
            total_pages = exchange.offered_book.total_pages or 100
            missing_percent = (exchange.pages_missing / total_pages) * 100
            offered_price -= (base_price * 0.005 * missing_percent)

            condition_adjustment = {
                "excellent": 0.01,
                "fine": 0.03,
                "not_good": 0.05
            }
            offered_price -= base_price * condition_adjustment.get(exchange.condition, 0)

            offered_price = max(0, offered_price)
            exchange.calculated_price = int(offered_price)
            requested_price = exchange.requested_book.price
            exchange.final_payment = int(requested_price - offered_price)

            exchange.save()

            return render(request, "exchange/result.html", {"exchange": exchange})
    else:
        form = ExchangeRequestForm()

    return render(request, "exchange/exchange_form.html", {"form": form})
