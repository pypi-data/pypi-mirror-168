import logging

from django.http import HttpRequest

logger = logging.getLogger(__name__)


def get_client_ip(request: HttpRequest):
    """
    type: (WSGIRequest) -> Optional[Any]
    Naively yank the first IP address in an X-Forwarded-For header
    and assume this is correct.

    Note: Don't use this in security sensitive situations since this
    value may be forged from a client.
    """
    for x in [
        "HTTP_X_ORIGINAL_FORWARDED_FOR",
        "HTTP_X_FORWARDED_FOR",
        "HTTP_X_REAL_IP",
        "REMOTE_ADDR",
    ]:
        ip = request.META.get(x)
        if ip:
            if "," in ip:
                return ip.split(",")[0].strip()
            return ip


def parse_bool(value):
    return value in [True, "True", "true", "T", "1", 1, "y", "Y"]
