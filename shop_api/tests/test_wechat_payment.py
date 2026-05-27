import hashlib
import pytest
from unittest.mock import MagicMock
from django.test import override_settings
from apps.payment.backends.wechat import WechatPaymentBackend


WECHAT_SANDBOX_SETTINGS = {
    "WECHAT_PAY": {
        "APPID": "wx_test_appid",
        "MCH_ID": "1234567890",
        "API_KEY": "test_api_key_123",
        "NOTIFY_URL": "https://example.com/wechat/notify",
        "SANDBOX": True,
    }
}

WECHAT_PROD_SETTINGS = {
    "WECHAT_PAY": {
        "APPID": "wx_prod_appid",
        "MCH_ID": "0987654321",
        "API_KEY": "prod_api_key_456",
        "NOTIFY_URL": "https://example.com/wechat/notify",
        "SANDBOX": False,
    }
}


@pytest.fixture
def backend():
    return WechatPaymentBackend()


@pytest.fixture
def mock_order():
    order = MagicMock()
    order.order_no = "ORD20260527001"
    return order


@pytest.mark.django_db
class TestWechatSandbox:
    @override_settings(**WECHAT_SANDBOX_SETTINGS)
    def test_create_payment_returns_pending(self, backend, mock_order):
        result = backend.create_payment(mock_order, "PAY001", 10000)
        assert result["status"] == "pending"
        assert result["payment_no"] == "PAY001"
        assert "pay_url" in result

    @override_settings(**WECHAT_SANDBOX_SETTINGS)
    def test_create_payment_pay_url_format(self, backend, mock_order):
        result = backend.create_payment(mock_order, "PAY002", 5000)
        assert result["pay_url"] == "weixin://wxpay/bizpayurl?pr=PAY002"

    @override_settings(**WECHAT_SANDBOX_SETTINGS)
    def test_query_payment_returns_success(self, backend):
        result = backend.query_payment("PAY001")
        assert result["status"] == "success"
        assert result["payment_no"] == "PAY001"

    @override_settings(**WECHAT_SANDBOX_SETTINGS)
    def test_verify_notification_sandbox_auto_succeeds(self, backend):
        data = {
            "out_trade_no": "PAY001",
            "result_code": "SUCCESS",
            "transaction_id": "TXN123",
        }
        result = backend.verify_notification(data)
        assert result["verified"] is True
        assert result["out_trade_no"] == "PAY001"
        assert result["trade_no"] == "TXN123"
        assert result["trade_status"] == "SUCCESS"

    @override_settings(**WECHAT_SANDBOX_SETTINGS)
    def test_verify_notification_fail_result(self, backend):
        data = {
            "out_trade_no": "PAY002",
            "result_code": "FAIL",
            "transaction_id": "",
        }
        result = backend.verify_notification(data)
        assert result["verified"] is True
        assert result["trade_status"] == "FAIL"

    @override_settings(**WECHAT_SANDBOX_SETTINGS)
    def test_refund_returns_not_supported(self, backend):
        result = backend.refund(MagicMock(), 1000)
        assert result["status"] == "not_supported"


@pytest.mark.django_db
class TestWechatProduction:
    @override_settings(**WECHAT_PROD_SETTINGS)
    def test_create_payment_builds_params(self, backend, mock_order):
        result = backend.create_payment(mock_order, "PAY_PROD_001", 10000)
        assert result["status"] == "pending"
        assert result["payment_no"] == "PAY_PROD_001"

    @override_settings(**WECHAT_PROD_SETTINGS)
    def test_query_payment_pending_in_production(self, backend):
        result = backend.query_payment("PAY_PROD_001")
        assert result["status"] == "pending"

    @override_settings(**WECHAT_PROD_SETTINGS)
    def test_verify_notification_valid_signature(self, backend):
        api_key = "prod_api_key_456"
        params = {
            "appid": "wx_prod_appid",
            "mch_id": "0987654321",
            "out_trade_no": "PAY_PROD_001",
            "result_code": "SUCCESS",
            "transaction_id": "TXN_PROD_123",
        }
        # Compute expected sign
        raw = "&".join(f"{k}={v}" for k, v in sorted(params.items()) if v)
        raw += f"&key={api_key}"
        expected_sign = hashlib.md5(raw.encode("utf-8")).hexdigest().upper()

        data = {**params, "sign": expected_sign}
        result = backend.verify_notification(data)
        assert result["verified"] is True
        assert result["out_trade_no"] == "PAY_PROD_001"
        assert result["trade_status"] == "SUCCESS"

    @override_settings(**WECHAT_PROD_SETTINGS)
    def test_verify_notification_bad_signature(self, backend):
        data = {
            "appid": "wx_prod_appid",
            "mch_id": "0987654321",
            "out_trade_no": "PAY_PROD_001",
            "result_code": "SUCCESS",
            "transaction_id": "TXN_PROD_123",
            "sign": "WRONG_SIGNATURE",
        }
        result = backend.verify_notification(data)
        assert result["verified"] is False


@pytest.mark.django_db
class TestWechatSign:
    def test_sign_deterministic(self, backend):
        params = {"a": "1", "b": "2", "c": "3"}
        sign1 = backend._sign(params, "mykey")
        sign2 = backend._sign(params, "mykey")
        assert sign1 == sign2

    def test_sign_skips_empty_values(self, backend):
        params = {"a": "1", "b": "", "c": "3"}
        sign_no_empty = backend._sign(params, "mykey")
        params_full = {"a": "1", "c": "3"}
        sign_full = backend._sign(params_full, "mykey")
        assert sign_no_empty == sign_full

    def test_sign_is_uppercase_hex(self, backend):
        sign = backend._sign({"a": "1"}, "key")
        assert sign == sign.upper()
        assert len(sign) == 32  # MD5 hex digest length
