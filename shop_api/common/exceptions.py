from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            "code": response.status_code,
            "message": _get_error_message(response),
            "errors": response.data if isinstance(response.data, dict) else None,
        }
    return response


def _get_error_message(response):
    data = response.data
    if isinstance(data, dict):
        detail = data.get("detail", "")
        if detail:
            return str(detail)
        # Flatten field errors into a readable message
        parts = []
        for field, errors in data.items():
            if isinstance(errors, list):
                parts.extend(errors)
            else:
                parts.append(str(errors))
        if parts:
            return parts[0]
    if isinstance(data, list):
        return data[0] if data else "请求错误"
    return str(data) if data else "请求错误"


class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "请求参数错误"
    default_code = "bad_request"


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "资源不存在"
    default_code = "not_found"
