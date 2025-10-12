from django.urls import path
from . import views

app_name = 'payment'  # This is the namespace for {% url %} usage

urlpatterns = [
    # Initiate payment for a specific object (exchange or sell)
    path("initiate/<str:payment_type>/<int:obj_id>/", views.initiate_payment, name="initiate"),

    # Payment success callback
    path("success/<str:transaction_id>/", views.payment_success, name="success"),

    # Payment fail callback
    path("fail/<str:transaction_id>/", views.payment_fail, name="fail"),

    # Payment cancelled callback
    path("cancel/<str:transaction_id>/", views.payment_cancel, name="cancel"),
]
