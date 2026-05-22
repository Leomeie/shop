from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("create/", views.PaymentCreateView.as_view(), name="payment_create"),
    path("callback/", views.PaymentCallbackView.as_view(), name="payment_callback"),
    path("alipay/notify/", views.AlipayNotifyView.as_view(), name="alipay_notify"),
    path("<str:payment_no>/", views.PaymentQueryView.as_view(), name="payment_query"),
]
