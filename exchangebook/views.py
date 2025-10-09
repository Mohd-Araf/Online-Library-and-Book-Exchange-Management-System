from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ExchangeRequestForm

def search_books(request):
    return render(request, "exchange/search.html")


@login_required(login_url="/accounts/login/")
def exchange_book(request):
    if request.method == "POST":
        form = ExchangeRequestForm(request.POST, request.FILES)
        if form.is_valid():
            exchange = form.save(commit=False)


            base_price = exchange.offered_book.base_price
            offered_price = base_price * 0.6
            offered_edition = exchange.offered_book.edition or 1
            requested_edition = exchange.requested_book.edition or 1
            edition_diff = abs(requested_edition - offered_edition )
            offered_price -= (base_price * 0.05 * edition_diff)

            total_pages = exchange.offered_book.total_pages or 100
            missing_percent = (exchange.pages_missing / total_pages) * 100
            offered_price -= (base_price * 0.005 * missing_percent)

            if exchange.condition == "excellent":
                offered_price -= base_price * 0.01
            elif exchange.condition == "fine":
                offered_price -= base_price * 0.03
            elif exchange.condition == "not_good":
                offered_price -= base_price * 0.05

            # Prevent negative price
            if offered_price < 0:
                offered_price = 0

            # Final payment calculation
            requested_price = exchange.requested_book.base_price
            final_payment = requested_price - offered_price

            # Save
            exchange.edition_difference = edition_diff
            exchange.calculated_price = int(offered_price)
            exchange.final_payment = int(final_payment)
            exchange.save()

            return render(request, "exchange/result.html", {"exchange": exchange})
    else:
        form = ExchangeRequestForm()

    return render(request, "exchange/exchange_form.html", {"form": form})