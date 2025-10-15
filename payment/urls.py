from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("initiate/<str:payment_type>/<int:obj_id>/", views.initiate_payment, name="initiate"),
    path("success/<uuid:transaction_id>/", views.payment_success, name="success"),
    path("success/page/<uuid:transaction_id>/", views.payment_success_page, name="success-page"),
    path("fail/<uuid:transaction_id>/", views.payment_fail, name="fail"),
    path("cancel/<uuid:transaction_id>/", views.payment_cancel, name="cancel"),
]
