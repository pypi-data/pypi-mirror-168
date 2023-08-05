import logging
import os
import re

from django.conf import settings
from django.utils.functional import SimpleLazyObject, cached_property
from django.utils.module_loading import import_string
from django_regex.utils import RegexList
from front_door.utils import parse_bool

FRONT_DOOR_CONFIG = getattr(settings, "FRONT_DOOR_CONFIG", "front_door.conf.DjangoSettings")

logger = logging.getLogger(__name__)


class FrontDoorConfig:
    defaults = dict(
        ALLOWED_PATHS=[],  # url paths regex list always allowed
        ENABLED=False,  # FrontDoor enable/disable
        FORBIDDEN_PATHS=[],  # url paths regex list always denied
        ALLOWED_IPS=[],  # allowed ips
        RULES=[
            "front_door.rules.forbidden_path",
            "front_door.rules.allowed_ip",
            "front_door.rules.internal_ip",
            "front_door.rules.allowed_path",
            "front_door.rules.special_header",
            "front_door.rules.cookie_value",
        ],
        ROUTER="front_door.router.DefaultRouter",
        HEADER=None,  # special header name without HTTP- prefix
        TOKEN=None,  # custom header value
        REDIR_URL="",
        ERROR_CODE=404,
        COOKIE_NAME=None,
        COOKIE_PATTERN=None,
    )

    def __init__(self) -> None:
        super().__init__()
        from django.core.signals import setting_changed
        setting_changed.connect(self.on_setting_changed)

    def _get(self, key):
        return self.defaults.get(key, None)

    def _get_list(self, key):
        custom = self._get(key)
        if isinstance(custom, (list, tuple)):
            return custom
        elif isinstance(custom, str):
            return custom.split(";")
        else:
            return []

    def __getattr__(self, key):
        if key in self.defaults.keys():
            return self._get(key)
        raise AttributeError(key)

    @cached_property
    def COOKIE_PATTERN(self):
        try:
            return re.compile(self._get("COOKIE_PATTERN"))
        except (TypeError, re.error):
            return None

    @cached_property
    def ALLOWED_PATHS(self):
        rules = RegexList([])
        for rule in self._get_list('ALLOWED_PATHS'):
            if rule:
                try:
                    rules.append(rule)
                except Exception as e:
                    logger.exception(e)
        return rules

    @cached_property
    def FORBIDDEN_PATHS(self):
        rules = RegexList([])
        for rule in self._get_list('FORBIDDEN_PATHS'):
            try:
                rules.append(rule)
            except Exception as e:
                logger.exception(e)
        return rules

    @cached_property
    def ALLOWED_IPS(self):
        return self._get_list('ALLOWED_IPS')

    @cached_property
    def ERROR_CODE(self):
        return int(self._get('ERROR_CODE'))

    @cached_property
    def ENABLED(self):
        return parse_bool(self._get('ENABLED'))

    @cached_property
    def allows(self):
        return [import_string(x) for x in self._get_list('RULES')]

    def on_setting_changed(self, **kwargs):
        self.invalidate()

    def invalidate(self):
        for attr in self.defaults.keys():
            try:
                delattr(self, attr)
            except AttributeError:
                pass


class DjangoSettings(FrontDoorConfig):
    def _get(self, key):
        full_name = f"FRONT_DOOR_{key}"
        return getattr(settings, full_name, super()._get(key))


class DjangoConstance(DjangoSettings):

    def __init__(self) -> None:
        import constance.signals
        super().__init__()

        constance.signals.config_updated.connect(self.on_setting_changed)
        self.storage = constance.config

    def _get(self, key):
        full_name = f"FRONT_DOOR_{key}"
        return getattr(self.storage, full_name, super()._get(key))


class OSEnv(FrontDoorConfig):
    def _get(self, key):
        full_name = f"FRONT_DOOR_{key}"
        return os.environ.get(full_name, self.defaults.get(key, None))


def get_config():
    return import_string(FRONT_DOOR_CONFIG)()


config = SimpleLazyObject(get_config)


def get_front_door_allowed_ips():
    return config.ALLOWED_IPS


def get_front_door_internal_ips():
    return settings.INTERNAL_IPS


def get_front_door_whitelisted_paths():
    return config.ALLOWED_PATHS


def get_front_door_forbidden_paths():
    return config.FORBIDDEN_PATHS


def front_door_is_active():
    return config.ENABLED
