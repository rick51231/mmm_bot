from django.utils.deprecation import MiddlewareMixin

from core.models import Settings


class CheckTokenMiddleware(MiddlewareMixin):

    def __call__(self, request):
        response = self.get_response(request)
        return response
