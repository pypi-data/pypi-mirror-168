import logging

from .conf import (config, front_door_is_active, get_front_door_allowed_ips,
                   get_front_door_forbidden_paths, get_front_door_internal_ips,
                   get_front_door_whitelisted_paths)
from .exception import FrontDoorClosed
from .utils import get_client_ip

logger = logging.getLogger(__name__)
logger_allow = logging.getLogger(f"{__name__}.allow")
logger_denied = logging.getLogger(f"{__name__}.denied")


def allowed_ip(request, ip, path, **kwargs):
    return ip in get_front_door_allowed_ips()


def internal_ip(request, ip, path, **kwargs):
    return ip in get_front_door_internal_ips()


def special_header(request, ip, path, **kwargs):
    if config.HEADER and config.TOKEN:
        return request.headers.get(config.HEADER) == config.TOKEN


def allowed_path(request, ip, path, **kwargs):
    return path in get_front_door_whitelisted_paths()


def forbidden_path(request, ip, path, **kwargs):
    if path in get_front_door_forbidden_paths():
        raise FrontDoorClosed


def cookie_exists(request, ip, path, **kwargs):
    return config.COOKIE_NAME in request.COOKIES


def cookie_value(request, ip, path, **kwargs):
    if not config.COOKIE_PATTERN and config.COOKIE_NAME:
        return False
    try:
        value = request.COOKIES[str(config.COOKIE_NAME)]
    except KeyError:
        return False
    return bool(config.COOKIE_PATTERN.match(value))


def front_door_allows_request(request):
    access_allowed = not front_door_is_active()
    if access_allowed:
        logger.debug("FrontDoor disabled")
    else:
        ip = get_client_ip(request)
        path = request.path

        for check in config.allows:
            try:
                if check(request, ip, path):
                    logger_allow.info(f"FrontDoor access ALLOWED by '{check.__name__}()' to {path}")
                    access_allowed = True
                    break
                else:
                    logger_denied.debug(f"FrontDoor access NOT GRANTED by '{check.__name__}()' to {path}")
            except FrontDoorClosed:
                logger_denied.debug(f"FrontDoor access FORBIDDEN by '{check.__name__}()' to {path}")
                return False

        # logger.error(f"FrontDoor refused access from {ip} to '{path}'")
    return access_allowed
