import telebot
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from bot import *
from core.middleware import CheckTokenMiddleware
import json


class HomeView(View):

    def get(self, request, **kwargs):
        print(self.request.GET)
        return HttpResponse()


class BotView(CheckTokenMiddleware, View):

    def post(self, request, **kwargs):
        bot = TeleBot()
        data = json.loads(self.request.body)
        update = telebot.types.Update.de_json(data)
        bot.process_new_updates([update])
        return HttpResponse()
