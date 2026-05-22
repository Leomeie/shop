import base64
import logging
from django.conf import settings
from .base import PaymentBackend

logger = logging.getLogger(__name__)


def _format_pem_key(raw_key: str, key_type: str) -> str:
    """Ensure a PEM key has proper headers, footers, and line breaks.
    Automatically converts PKCS#8 private keys to PKCS#1 for Alipay SDK compatibility.
    """
    raw = raw_key.strip()

    # Already has PEM headers
    if raw.startswith("-----"):
        pem = raw
    else:
        # Raw base64 — wrap with headers
        b64 = "".join(raw.split())
        lines = [b64[i:i+64] for i in range(0, len(b64), 64)]
        if key_type == "private":
            pem = "\n".join(["-----BEGIN PRIVATE KEY-----"] + lines + ["-----END PRIVATE KEY-----"])
        else:
            pem = "\n".join(["-----BEGIN PUBLIC KEY-----"] + lines + ["-----END PUBLIC KEY-----"])

    # Convert PKCS#8 → PKCS#1 for private keys (Alipay SDK requires PKCS#1)
    if key_type == "private" and "BEGIN PRIVATE KEY" in pem:
        try:
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.backends import default_backend

            private_key = serialization.load_pem_private_key(
                pem.encode(), password=None, backend=default_backend()
            )
            pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            ).decode()
            logger.info("Converted PKCS#8 private key to PKCS#1")
        except Exception:
            logger.exception("Failed to convert PKCS#8 to PKCS#1")

    return pem


class AlipayPaymentBackend(PaymentBackend):
    """Alipay sandbox payment backend — lazy client init."""

    def _get_client(self):
        from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
        from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient

        cfg = settings.ALIPAY
        alipay_client_config = AlipayClientConfig()
        alipay_client_config.server_url = cfg["GATEWAY"]
        alipay_client_config.app_id = cfg["APPID"]
        alipay_client_config.app_private_key = _format_pem_key(cfg["APP_PRIVATE_KEY"], "private")
        alipay_client_config.alipay_public_key = _format_pem_key(cfg["ALIPAY_PUBLIC_KEY"], "public")

        return DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)

    def create_payment(self, order, payment_no, amount) -> dict:
        from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
        from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest

        client = self._get_client()

        model = AlipayTradePagePayModel()
        model.out_trade_no = payment_no
        model.total_amount = f"{amount / 100:.2f}"
        model.subject = f"订单 {order.order_no}"
        model.product_code = "FAST_INSTANT_TRADE_PAY"

        request = AlipayTradePagePayRequest(biz_model=model)
        request.notify_url = settings.ALIPAY["NOTIFY_URL"]
        request.return_url = settings.ALIPAY["RETURN_URL"]

        response = client.page_execute(request, http_method="GET")
        return {
            "payment_no": payment_no,
            "status": "pending",
            "pay_url": response,
        }

    def query_payment(self, payment_no) -> dict:
        from alipay.aop.api.domain.AlipayTradeQueryModel import AlipayTradeQueryModel
        from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest
        from alipay.aop.api.response.AlipayTradeQueryResponse import AlipayTradeQueryResponse

        client = self._get_client()

        model = AlipayTradeQueryModel()
        model.out_trade_no = payment_no

        request = AlipayTradeQueryRequest(biz_model=model)

        response_content = client.execute(request)
        response = AlipayTradeQueryResponse()
        response.parse_response_content(response_content)

        status_map = {
            "TRADE_SUCCESS": "success",
            "TRADE_FINISHED": "success",
        }
        return {
            "payment_no": payment_no,
            "status": status_map.get(response.trade_status, "pending"),
        }

    def refund(self, payment, amount) -> dict:
        return {"status": "not_supported"}

    def verify_callback(self, data: dict) -> dict:
        """Verify Alipay async notification RSA2 signature."""
        sign = data.get("sign", "")
        sign_type = data.get("sign_type", "RSA2")

        # Filter out sign and sign_type, sort by key
        filtered = "&".join(
            f"{k}={v}" for k, v in sorted(data.items())
            if v and k not in ("sign", "sign_type")
        )

        try:
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.backends import default_backend

            # Format the public key
            pub_key_str = _format_pem_key(settings.ALIPAY["ALIPAY_PUBLIC_KEY"], "public")

            public_key = serialization.load_pem_public_key(
                pub_key_str.encode(), backend=default_backend()
            )

            # Decode the base64 signature
            signature = base64.b64decode(sign)

            # Verify
            public_key.verify(
                signature,
                filtered.encode("utf-8"),
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
            verified = True
        except Exception:
            logger.exception("Alipay signature verification failed")
            verified = False

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
