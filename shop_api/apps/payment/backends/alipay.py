import logging
from django.conf import settings
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradeQueryModel import AlipayTradeQueryModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest
from .base import PaymentBackend

logger = logging.getLogger(__name__)


class AlipayPaymentBackend(PaymentBackend):
    """Alipay sandbox payment backend."""

    def __init__(self):
        cfg = getattr(settings, "ALIPAY", {})
        self._client = DefaultAlipayClient(
            app_id=cfg["APPID"],
            app_private_key_string=cfg["APP_PRIVATE_KEY"],
            alipay_public_key_string=cfg["ALIPAY_PUBLIC_KEY"],
            sign_type="RSA2",
            gateway_url=cfg.get("GATEWAY", "https://openapi-sandbox.dl.alipaydev.com/gateway.do"),
        )

    def create_payment(self, order, payment_no, amount) -> dict:
        model = AlipayTradePagePayModel()
        model.out_trade_no = payment_no
        model.total_amount = f"{amount / 100:.2f}"
        model.subject = f"订单 {order.order_no}"
        model.product_code = "FAST_INSTANT_TRADE_PAY"

        request = AlipayTradePagePayRequest(biz_model=model)
        request.notify_url = f"{settings.ALIPAY['NOTIFY_URL']}"
        request.return_url = f"{settings.ALIPAY['RETURN_URL']}"

        response = self._client.page_execute(request, http_method="GET")
        return {
            "payment_no": payment_no,
            "status": "pending",
            "pay_url": response,
        }

    def query_payment(self, payment_no) -> dict:
        model = AlipayTradeQueryModel()
        model.out_trade_no = payment_no

        request = AlipayTradeQueryRequest(biz_model=model)
        response = self._client.page_execute(request, http_method="GET")

        # Parse response
        if isinstance(response, dict):
            trade_status = response.get("trade_status", "")
        else:
            trade_status = ""

        status_map = {
            "TRADE_SUCCESS": "success",
            "TRADE_FINISHED": "success",
        }
        return {
            "payment_no": payment_no,
            "status": status_map.get(trade_status, "pending"),
        }

    def refund(self, payment, amount) -> dict:
        # TODO: implement Alipay refund if needed
        return {"status": "not_supported"}

    def verify_callback(self, data: dict) -> dict:
        """Verify Alipay async notification signature and return parsed data."""
        verified = self._client.verify(data)
        if not verified:
            logger.warning("Alipay callback signature verification failed")
            return {"verified": False}

        return {
            "verified": True,
            "out_trade_no": data.get("out_trade_no"),
            "trade_no": data.get("trade_no"),
            "trade_status": data.get("trade_status"),
            "total_amount": data.get("total_amount"),
        }
