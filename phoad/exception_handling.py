from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework.views import exception_handler

from photosmap.dto import InvalidLocationArguments


def validation_exception_handler(ex, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(ex, context)
    if response and not is_2xx_family(response.status_code):
        return response

    headers = response.headers if hasattr(response, 'headers') else None
    if isinstance(ex, InvalidLocationArguments):
        response = Response(data=to_error_detail(ex), status=400, headers=headers)
    return response


def is_2xx_family(status_code):
    return status_code // 100 == 2


def to_error_detail(ex):
    return {'detail': ErrorDetail(str(ex))}
