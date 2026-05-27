import hashlib
import logging
import time
import xml.etree.ElementTree as ET

from django.conf import settings
from .base import PaymentBackend

logger = logging.getLogger(__name__)

WECHAT_API_BASE = "https://api.mch.weixin.qq.com"


class WechatPaymentBackend(PaymentBackend):
    """WeChat Pay sandbox payment backend.

    In sandbox mode, create_payment returns a mock URL and
    verify_notification auto-succeeds. Replace with real SDK
    calls for production.
    """

    def _get_config(self):
        cfg = getattr(settings, "WECHAT_PAY", {})
        return {
            "appid": cfg.get("APPID", ""),
            "mch_id": cfg.get("MCH_ID", ""),
            "api_key": cfg.get("API_KEY", ""),
            "notify_url": cfg.get("NOTIFY_URL", ""),
            "sandbox": cfg.get("SANDBOX", True),
        }

    def create_payment(self, order, payment_no, amount) -> dict:
        cfg = self._get_config()

        if cfg["sandbox"]:
            pay_url = f"weixin://wxpay/bizpayurl?pr={payment_no}"
            logger.info("WeChat sandbox payment created: %s", payment_no)
            return {
                "payment_no": payment_no,
                "status": "pending",
                "pay_url": pay_url,
            }

        # Production: build unified order params and sign
        params = {
            "appid": cfg["appid"],
            "mch_id": cfg["mch_id"],
            "nonce_str": hashlib.md5(f"{payment_no}{time.time()}".encode()).hexdigest(),
            "body": f"订单 {order.order_no}",
            "out_trade_no": payment_no,
            "total_fee": amount,
            "notify_url": cfg["notify_url"],
            "trade_type": "NATIVE",
        }
        params["sign"] = self._sign(params, cfg["api_key"])

        # In production, POST to https://api.mch.weixin.qq.com/pay/unifiedorder
        # and parse XML response. For now, return pending with a placeholder.
        logger.info("WeChat payment created: %s", payment_no)
        return {
            "payment_no": payment_no,
            "status": "pending",
            "pay_url": f"weixin://wxpay/bizpayurl?pr={payment_no}",
        }

    def query_payment(self, payment_no) -> dict:
        cfg = self._get_config()

        if cfg["sandbox"]:
            return {
                "payment_no": payment_no,
                "status": "success",
            }

        # Production: POST to https://api.mch.weixin.qq.com/pay/orderquery
        return {
            "payment_no": payment_no,
            "status": "pending",
        }

    def refund(self, payment, amount) -> dict:
        return {"status": "not_supported"}

    def verify_notification(self, data: dict) -> dict:
        """Verify WeChat Pay async notification.

        In sandbox mode, auto-succeeds. In production, verifies
        the XML signature using MD5(HMAC-SHA256).
        """
        cfg = self._get_config()

        if cfg["sandbox"]:
            out_trade_no = data.get("out_trade_no", "")
            result_code = data.get("result_code", "SUCCESS")
            logger.info("WeChat sandbox notification: %s, result=%s", out_trade_no, result_code)
            return {
                "verified": True,
                "out_trade_no": out_trade_no,
                "trade_no": data.get("transaction_id", ""),
                "trade_status": "SUCCESS" if result_code == "SUCCESS" else "FAIL",
            }

        # Production: verify signature
        sign = data.get("sign", "")
        filtered = {k: v for k, v in data.items() if v and k not in ("sign", "sign_type")}
        expected_sign = self._sign(filtered, cfg["api_key"])

        if sign != expected_sign:
            logger.warning("WeChat notification signature mismatch: %s", data.get("out_trade_no"))
            return {"verified": False}

        return {
            "verified": True,
            "out_trade_no": data.get("out_trade_no"),
            "trade_no": data.get("transaction_id"),
            "trade_status": data.get("result_code"),
        }

    def _sign(self, params: dict, api_key: str) -> str:
        """Generate MD5 sign for WeChat Pay params."""
        raw = "&".join(f"{k}={v}" for k, v in sorted(params.items()) if v)
        raw += f"&key={api_key}"
        return hashlib.md5(raw.encode("utf-8")).hexdigest().upper()
