from django.utils import timezone
from .base import PaymentBackend


class MockPaymentBackend(PaymentBackend):
    """Mock payment backend for development — auto-succeeds."""

    def create_payment(self, order, payment_no, amount) -> dict:
        return {
            "payment_no": payment_no,
            "status": "pending",
            "pay_url": f"/mock-pay/{payment_no}",
        }

    def query_payment(self, payment_no) -> dict:
        return {
            "payment_no": payment_no,
            "status": "success",
            "paid_at": timezone.now(),
        }

    def refund(self, payment, amount) -> dict:
        return {
            "status": "success",
            "refund_no": f"REF{payment.payment_no}",
        }
