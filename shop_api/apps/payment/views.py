from django.db import models
from django.utils import timezone
from rest_framework import permissions
from rest_framework.views import APIView
from .models import Payment
from .backends.mock import MockPaymentBackend
from apps.orders.models import Order
from common.utils import generate_payment_no
from common.response import success, error

BACKENDS = {
    "mock": MockPaymentBackend(),
}


def get_backend(method="mock"):
    return BACKENDS.get(method, BACKENDS["mock"])


class PaymentCreateView(APIView):
    """Create a payment for an order."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")
        method = request.data.get("method", "mock")

        order = Order.objects.filter(pk=order_id, user=request.user, status="pending", is_deleted=False).first()
        if not order:
            return error("订单不存在或不在待支付状态")

        if Payment.objects.filter(order=order, status="success").exists():
            return error("订单已支付")

        payment_no = generate_payment_no()
        backend = get_backend(method)
        result = backend.create_payment(order, payment_no, order.pay_amount)

        payment = Payment.objects.create(
            order=order,
            payment_no=payment_no,
            amount=order.pay_amount,
            method=method,
        )

        return success({
            "payment_no": payment.payment_no,
            "amount": payment.amount,
            "amount_yuan": payment.amount / 100,
            "pay_url": result.get("pay_url"),
        })


class PaymentCallbackView(APIView):
    """Mock payment callback — simulates successful payment."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        payment_no = request.data.get("payment_no")
        if not payment_no:
            return error("缺少支付流水号")

        payment = Payment.objects.filter(payment_no=payment_no, status="pending").first()
        if not payment:
            return error("支付记录不存在或已处理")

        backend = get_backend(payment.method)
        result = backend.query_payment(payment_no)

        if result["status"] == "success":
            payment.status = "success"
            payment.paid_at = timezone.now()
            payment.save(update_fields=["status", "paid_at"])

            order = payment.order
            order.status = "paid"
            order.pay_time = timezone.now()
            order.save(update_fields=["status", "pay_time"])

            # Auto-complete digital orders
            order.status = "completed"
            order.complete_time = timezone.now()
            order.save(update_fields=["status", "complete_time"])

            # Increment download count on product
            for item in order.items.all():
                if item.sku and item.sku.product:
                    from apps.products.models import Product
                    Product.objects.filter(pk=item.sku.product_id).update(
                        download_count=models.F("download_count") + 1
                    )

            return success({"status": "completed"})
        else:
            payment.status = "failed"
            payment.save(update_fields=["status"])
            return error("支付失败")


class PaymentQueryView(APIView):
    """Query payment status."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, payment_no):
        payment = Payment.objects.filter(
            payment_no=payment_no, order__user=request.user,
        ).first()
        if not payment:
            return error("支付记录不存在")
        return success({
            "payment_no": payment.payment_no,
            "status": payment.status,
            "amount_yuan": payment.amount / 100,
            "paid_at": payment.paid_at,
        })
