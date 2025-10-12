import uuid
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
from sell_books.models import SellBook
from exchangebook.models import ExchangeRequest

# Store credentials from settings
STORE_ID = settings.SSL_COMMERZ_STORE_ID
STORE_PASSWORD = settings.SSL_COMMERZ_STORE_PASSWORD
API_URL = settings.SSL_COMMERZ_API_BASE_URL


@login_required
def initiate_payment(request, payment_type, obj_id):
    """
    Handles both SellBook and ExchangeBook payments.
    payment_type: 'sell' or 'exchange'
    obj_id: book_id or exchange_id
    """
    transaction_id = str(uuid.uuid4())

    if payment_type == "sell":
        book = get_object_or_404(SellBook, id=obj_id)
        amount = book.price
        payment = Payment.objects.create(
            user=request.user,
            transaction_id=transaction_id,
            amount=amount,
            sell_book=book
        )

    elif payment_type == "exchange":
        exchange = get_object_or_404(ExchangeRequest, id=obj_id)
        amount = exchange.final_payment
        payment = Payment.objects.create(
            user=request.user,
            transaction_id=transaction_id,
            amount=amount,
            exchange_request=exchange
        )

    else:
        return HttpResponse("Invalid Payment Type")

    # Payment URLs
    success_url = request.build_absolute_uri(f"/payment/success/{transaction_id}/")
    fail_url = request.build_absolute_uri(f"/payment/fail/{transaction_id}/")
    cancel_url = request.build_absolute_uri(f"/payment/cancel/{transaction_id}/")

    post_data = {
        "store_id": STORE_ID,
        "store_passwd": STORE_PASSWORD,
        "total_amount": str(amount),
        "currency": "BDT",
        "tran_id": transaction_id,
        "success_url": success_url,
        "fail_url": fail_url,
        "cancel_url": cancel_url,
        "cus_name": request.user.username,
        "cus_email": request.user.email,
        "cus_phone": "01700000000",
        "shipping_method": "NO",
        "product_name": payment_type.capitalize(),
        "product_category": "Online Library",
        "product_profile": "general",
    }

    response = requests.post(API_URL, data=post_data)
    response_data = response.json()

    if response_data.get('status') == 'SUCCESS':
        gateway_url = response_data['GatewayPageURL']
        return redirect(gateway_url)
    else:
        # Debug: SSLCommerz response
        print("SSLCommerz response:", response_data)
        return HttpResponse("Payment initialization failed. Please try again.")


@csrf_exempt
def payment_success(request, transaction_id):
    payment = get_object_or_404(Payment, transaction_id=transaction_id)
    payment.status = "Successful"
    payment.save()

    if payment.sell_book:
        return redirect('buy-success', buy_id=payment.sell_book.id)
    elif payment.exchange_request:
        return render(request, "payment/success.html", {
            "exchange": payment.exchange_request,
            "transaction_id": payment.transaction_id
        })

    return HttpResponse("Payment completed successfully.")


@csrf_exempt
def payment_fail(request, transaction_id):
    payment = get_object_or_404(Payment, transaction_id=transaction_id)
    payment.status = "Failed"
    payment.save()
    return render(request, "payment/fail.html", {"payment": payment})


@csrf_exempt
def payment_cancel(request, transaction_id):
    payment = get_object_or_404(Payment, transaction_id=transaction_id)
    payment.status = "Cancelled"
    payment.save()
    return render(request, "payment/cancel.html", {"payment": payment})
