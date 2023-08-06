from django.http import HttpResponse, HttpResponseRedirect

from .conf import config


class DefaultRouter:
    def route(self, request):
        if config.REDIR_URL:
            response = HttpResponseRedirect(config.REDIR_URL)
        else:
            response = HttpResponse("", status=config.ERROR_CODE)
        return response


router = DefaultRouter()
