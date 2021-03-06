from datetime import timedelta
from time import sleep

from celery import shared_task
from django.utils import timezone
from telebot import TeleBot

from core.models import Person, MessagePastFinish, Settings
from workers.celery_worker import celery
import traceback


@celery.task()
def send_notification_users():
    count_message_past_finish = MessagePastFinish.objects.count()
    message_past_finish = list(MessagePastFinish.objects.all())

    if count_message_past_finish:
        for person in Person.objects.all():
            sleep(1)
            if person.date_finish_task and person.bot:
                bot = TeleBot(person.bot.bot_id, threaded=False)
                for past_message in message_past_finish:
                    difference_time = timedelta(days=past_message.days, hours=past_message.hours,
                                                minutes=past_message.minute)
                    time_passed = timezone.now() - person.date_creation

                    if time_passed > difference_time and person not in past_message.sending.all():
                        try:
                            if past_message.video:
                                bot.send_message(person.chat_id, f"[Видео]({past_message.video})",
                                                 parse_mode='Markdown')
                            bot.send_message(person.chat_id, f"{past_message.text}\n", disable_web_page_preview=True)
                        except Exception as error:
                            print(error)
                            traceback.print_exc()

                        past_message.sending.add(person)
                        past_message.save()
