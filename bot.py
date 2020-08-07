import os
import re
import time

from django import setup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

setup()

from django.utils import timezone
from core.models import Person, Settings
from django.db import IntegrityError
from core.settings import VIDEO_DATA_SELECT, VIDEO_STEP_1, VIDEO_STEP_2, VIDEO_STEP_3, COMPANY_URL, TEXT_STEP_1, \
    TEXT_STEP_2, TEXT_STEP_4
from telebot import TeleBot, types

settings = Settings.get()

bot = TeleBot(settings.bot_id, threaded=False)
bot.set_webhook()


def referral_id(text):
    return text.split()[1] if len(text.split()) > 1 else None


@bot.message_handler(commands=['start'])
def start(message):
    referral_link = referral_id(message.text)
    if referral_link:
        referrer = Person.objects.filter(system_id=referral_link).first()
    else:
        referrer = None
    person, person_create = Person.objects.get_or_create(telegram_id=message.from_user.id)
    person.first_name = message.from_user.first_name
    person.last_name = message.from_user.last_name
    person.username = message.from_user.username
    if person.referrer is None:
        person.referrer = referrer
    person.chat_id = message.chat.id
    person.current_step = 0
    person.date_finish_task = timezone.now()
    person.save()

    inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
    inline_buttons = [types.InlineKeyboardButton(text=key, callback_data=key) for key, value in
                      VIDEO_DATA_SELECT.items()]

    inline_keyboard.add(*inline_buttons)
    bot.send_message(message.chat.id, f'{message.from_user.first_name} {message.from_user.last_name},'
                                      f' в какой теме вы больше видите себя?', reply_markup=inline_keyboard)


@bot.callback_query_handler(func=lambda mess: mess.data in VIDEO_DATA_SELECT.keys())
def step_1(call):
    person, _ = Person.objects.get_or_create(telegram_id=call.from_user.id)
    person.current_step = 1
    person.select_video = call.data
    person.save()
    chat_id = call.message.chat.id
    inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
    inline_keyboard.add(types.InlineKeyboardButton(text='Перейти к "Шаг 2"', callback_data="step_2"))
    text = f'*Шаг 1*'
    bot.send_message(chat_id, text, parse_mode='Markdown')

    text = f'{TEXT_STEP_1}' \
           f'[!]({VIDEO_STEP_1})'

    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=inline_keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'step_2')
def step_2(call):
    person, _ = Person.objects.get_or_create(telegram_id=call.from_user.id)
    person.current_step = 2
    person.save()
    chat_id = call.message.chat.id
    text = f'*Шаг 2*'
    bot.send_message(chat_id, text, parse_mode='Markdown')

    inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
    inline_keyboard.add(
        types.InlineKeyboardButton(text='Перейти к "Шаг 3"',
                                   callback_data="step_3", )
    )
    text = f'{TEXT_STEP_2}' \
           f'[!]({VIDEO_STEP_2})'
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=inline_keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'step_3')
def step_3(call):
    person, _ = Person.objects.get_or_create(telegram_id=call.from_user.id)
    person.current_step = 3
    person.save()
    chat_id = call.message.chat.id

    referral = f"{person.referrer.system_id}/" if person.referrer else ""
    text = f'*Шаг 3*'
    bot.send_message(chat_id, text, parse_mode='Markdown')

    inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
    inline_keyboard.add(
        types.InlineKeyboardButton(text='Попробовать бесплатно',
                                   callback_data="bonus",
                                   url=f"{COMPANY_URL}{referral}"),
    )
    text = f'Остался последний шаг, свяжись со своим куратором' \
           f'[.]({VIDEO_STEP_3})'
    bot.send_message(chat_id, f'{text}', parse_mode="Markdown", reply_markup=inline_keyboard)

    text = 'Не забудь отправить свой ID для перехода к "Шаг 4"'
    bot.send_message(chat_id, f'{text}', parse_mode="Markdown")


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    person, _ = Person.objects.get_or_create(telegram_id=message.from_user.id)
    if person.current_step == 3:
        person.system_id = message.text
        try:
            person.save()
        except IntegrityError:
            text = 'Данный ID уже зарегистрирован в системе, ' \
                   'отправте ваш ID'
            bot.send_message(message.chat.id, text)
        else:
            text = 'Ваш ID сохранен, если вы ввели неверный ID, ' \
                   'просто отправте заново мы перезапишем его'
            inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
            inline_keyboard.add(
                types.InlineKeyboardButton(text='Подтвердить',
                                           callback_data="step_3_confirm", )
            )

            bot.send_message(message.chat.id, text, reply_markup=inline_keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'step_3_confirm')
def step_3_confirm(call):
    person, _ = Person.objects.get_or_create(telegram_id=call.from_user.id)
    person.current_step = 4
    person.save()

    referrer = person.referrer
    chat_id = call.message.chat.id

    if referrer is not None:
        inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
        inline_keyboard.add(
            types.InlineKeyboardButton(text='Верифицировать', callback_data=f"step_3_accept_{person.telegram_id}"),
            types.InlineKeyboardButton(text='Отменить', callback_data=f"step_3_ban_{person.telegram_id}"),
        )

        bot.send_message(referrer.chat_id, text=f"У вас новый пользователь \n"
                                                f"Данные: {person.first_name} {person.last_name} \n"
                                                f"ID: {person.system_id}\n"
                                                f"@{person.username}\n",
                         reply_markup=inline_keyboard)
        text = 'Ожидайте подтверждения от вашего куратора'
        bot.edit_message_text(text, chat_id=chat_id, message_id=call.message.message_id)
    else:
        step_4_part(person)


@bot.callback_query_handler(func=lambda call: re.search(r'step_3_accept_\w+', call.data))
def step_3_accept(call):
    referrer_id = call.data.split('step_3_accept_')[1]
    person, _ = Person.objects.get_or_create(telegram_id=call.from_user.id)
    referrer = person.referral_users.filter(telegram_id=referrer_id).first()
    if referrer is not None:
        step_4_part(referrer)

        chat_id = call.message.chat.id
        text = f'Заявка @{referrer.username} принята\n' \
               f'ID: {referrer.system_id}'
        bot.edit_message_text(text, chat_id=chat_id, message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: re.search(r'step_3_ban_\w+', call.data))
def step_3_ban(call):
    referrer_id = call.data.split('step_3_ban_')[1]
    person, _ = Person.objects.get_or_create(telegram_id=call.from_user.id)
    referrer = person.referral_users.filter(telegram_id=referrer_id).first()
    if referrer is not None:
        referrer.current_step = 3
        referrer.save()
        text = f'Ваша заявка была отменена, проверьте ваш ID и отправьте заново'
        bot.send_message(referrer.chat_id, text=text, parse_mode="Markdown")

        chat_id = call.message.chat.id
        text = f'Заявка @{referrer.username} отклонена\n' \
               f'ID: {referrer.system_id}'
        bot.edit_message_text(text, chat_id=chat_id, message_id=call.message.message_id)


def step_4_part(person):
    chat_id = person.chat_id
    person.current_step = 5
    person.save()
    bonus_link = settings.bonus_link or '' if settings else ''
    text = f'*Шаг 4*'
    bot.send_message(chat_id, text, parse_mode='Markdown')

    inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
    inline_keyboard.add(types.InlineKeyboardButton(text='Получить бонус', url=f"{bonus_link}"), )
    default_video = VIDEO_DATA_SELECT[list(VIDEO_DATA_SELECT.keys())[0]] if VIDEO_DATA_SELECT.keys() else ""

    text = f'{TEXT_STEP_4}' \
           f'[!]({VIDEO_DATA_SELECT.get(person.select_video, default_video)})'
    bot.send_message(chat_id, f'{text}', parse_mode="Markdown", reply_markup=inline_keyboard)
    text = f"Пригласи друга: {settings.ref_link}?start={person.system_id}"
    bot.send_message(chat_id, text)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)

        except Exception as e:
            print(e)
            time.sleep(5)
