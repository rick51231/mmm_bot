from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import FileField
from core.settings import WEBHOOK_URL


class Person(models.Model):
    telegram_id = models.CharField(verbose_name="Telegram id", max_length=128, unique=True)
    system_id = models.CharField(verbose_name="ID в системе", max_length=128, null=True, blank=True)
    chat_id = models.CharField(verbose_name="ID чата", max_length=256, null=True, blank=True)
    referrer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="referral_users", verbose_name="Куратор")
    first_name = models.CharField(verbose_name="Имя", max_length=128, null=True, blank=True)
    last_name = models.CharField(verbose_name="Фамилия", max_length=128, null=True, blank=True)
    username = models.CharField(verbose_name="Username", max_length=128, null=True, blank=True)
    select_video = models.CharField("Выбранное видео", max_length=256, null=True, blank=True)
    current_step = models.IntegerField("Текущий шаг", default=0)
    date_creation = models.DateTimeField(verbose_name='Дата и время создания', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name='Дата и время последнего изменения', auto_now=True)
    date_finish_task = models.DateTimeField(verbose_name='Дата и время окончания теста', null=True, blank=True)

    def __str__(self):
        return f"{self.telegram_id} {self.first_name} {self.last_name} {self.username}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @classmethod
    def update_status(cls, telegram_id, current_step):
        obj, _ = cls.objects.get_or_create(telegram_id=telegram_id)
        obj.current_step = current_step
        obj.save()
        return obj


class Video(models.Model):
    video = FileField(verbose_name="Файл")
    telegram_id = models.CharField("ID в телеграмме", max_length=256, null=True, blank=True)
    file_id = models.IntegerField(verbose_name="id файла", null=True, blank=True)
    name = models.CharField("Имя файла", max_length=256, null=True, blank=True)


class Settings(models.Model):
    bot_id = models.CharField(max_length=128, verbose_name="ID бота", unique=True)
    bonus_link = models.CharField(max_length=1000, verbose_name="Ссылка на бонус", null=True, blank=True)
    ref_link = models.CharField(max_length=1000, verbose_name='Реферальная ссылка')

    @classmethod
    def get(cls):
        return cls._default_manager.all().first()

    def save(self, *args, **kwargs):
        from bot import bot
        if not self.pk and Settings.objects.exists():
            raise ValidationError('There is can be only one Settings')
        bot.token = self.bot_id
        bot.set_webhook(url=f"{WEBHOOK_URL}/bot/{self.bot_id}/")
        return super(Settings, self).save(*args, **kwargs)

    def __str__(self):
        return "Изменить настройки"

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"


class MessagePastFinish(models.Model):
    text = models.TextField(verbose_name="Текст сообщения")
    video = models.TextField(verbose_name="Ссылка на видео")

    minute = models.IntegerField(verbose_name="Минут", default=0)
    hours = models.IntegerField(verbose_name="Часов", default=0)
    days = models.IntegerField(verbose_name="Дней", default=0)
    sending = models.ManyToManyField(Person, verbose_name="Уже отправленно", default=[], blank=True)

    def __str__(self):
        return f"{self.days} {self.hours} {self.minute} {self.video}"

    class Meta:
        verbose_name = "Сообщение после прохождения теста"
        verbose_name_plural = "Сообщения после прохождения теста"
