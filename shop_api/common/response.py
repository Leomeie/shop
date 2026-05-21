from rest_framework.response import Response


def success(data=None, message="success", code=200):
    return Response({"code": code, "message": message, "data": data}, status=code)


def error(message="请求错误", code=400, errors=None):
    return Response({"code": code, "message": message, "errors": errors}, status=code)
