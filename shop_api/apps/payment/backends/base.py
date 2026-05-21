from abc import ABC, abstractmethod


class PaymentBackend(ABC):
    @abstractmethod
    def create_payment(self, order, payment_no, amount) -> dict:
        """Create a payment and return payment info."""

    @abstractmethod
    def query_payment(self, payment_no) -> dict:
        """Query payment status."""

    @abstractmethod
    def refund(self, payment, amount) -> dict:
        """Refund a payment."""
