from django.http import HttpResponse
from django.views import View


class HomeView(View):

    def get(self, request, **kwargs):
        print(self.request.GET)
        return HttpResponse()


class BotView(View):

    def get(self, request, **kwargs):
        print(self.request.GET)
        return HttpResponse()
