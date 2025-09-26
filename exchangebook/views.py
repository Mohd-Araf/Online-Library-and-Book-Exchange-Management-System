from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ExchangeRequestForm

def search_books(request):
    return render(request, "exchange/search.html")


@login_required(login_url="/accounts/login/")
def exchange_book(request):
    if request.method == "POST":
        form = ExchangeRequestForm(request.POST)
        if form.is_valid():
            exchange = form.save(commit=False)

            # Offered book base price
            base_price = exchange.offered_book.base_price
            offered_price = base_price * 0.5  # 50% cut

            # Pages missing → 2% cut each
            offered_price -= (exchange.pages_missing * (base_price * 0.02))

            # Edition difference → 3% cut each
            offered_price -= (exchange.edition_difference * (base_price * 0.03))

            # Condition cut
            if exchange.condition == "excellent":
                offered_price -= base_price * 0.03
            elif exchange.condition == "fine":
                offered_price -= base_price * 0.06
            elif exchange.condition == "not_good":
                offered_price -= base_price * 0.10

            if offered_price < 0:
                offered_price = 0

            requested_price = exchange.requested_book.base_price
            final_payment = requested_price - offered_price

            exchange.calculated_price = int(offered_price)
            exchange.final_payment = int(final_payment)
            exchange.save()

            return render(request, "exchange/result.html", {"exchange": exchange})
    else:
        form = ExchangeRequestForm()

    return render(request, "exchange/exchange_form.html", {"form": form})
