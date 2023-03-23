from django.db import models
from decimal import Decimal, DecimalTuple
from email.policy import default
from numbers import Integral
import random
from json import dumps
from unicodedata import decimal
from datetime import datetime, timedelta
from engine.messages import create_keyboard
# Create your models here.


class Account(models.Model):
    class TempData:
        bot = None

    class Dialog:
        START = 'start'
        DEFAULT = 'default'

    uid = models.TextField(default='', help_text='uid')
    register = models.TextField(default=datetime.now().strftime(
        "%H:%M:%S, %d.%m.%Y"), blank=True, help_text='Дата и время регистрации')
    last_peer_id = models.TextField(
        default=0, help_text='ID диалога, из которого пришло последнее сообщение')
    wrote_personal = models.BooleanField(
        default=False, help_text='Писал(-а) ли в личные сообщение?')
    messages_count = models.BigIntegerField(
        default=0, help_text='Количество сообщений')
    online_time = models.DateTimeField(
        default=datetime.now, help_text='Время онлайна')

    nickname = models.TextField(
        default='', null=True, blank=True, help_text='Никнейм')

    admin = models.BooleanField(default=False, help_text='Администратор')

    ban = models.BooleanField(default=False, help_text='Бан')

    # class Meta:
    #     verbose_name = "Пользователи"
    #     verbose_name_plural = "Пользователи"
    #     ordering = ("id", "uid", "register", "messages_count", "nickname", "status",
    #                 "gender", "admin", "balance", "bank", "bitcoins", "energy", "exp", "ban")

    async def reply(self, text=None, keyboard=None, inline=False, one_time=False, only_user=False, personal=False, **kwargs):
        if only_user:
            peer_id = self.uid
        else:
            peer_id = self.last_peer_id

        data = {'peer_id': peer_id, 'random_id': random.randint(
            1, 10000000), 'disable_mentions': 1}
        if text is not None:
            data['message'] = text
        if personal:
            personal = self.uid
        else:
            personal = None
        new_kb = create_keyboard(
            kb=keyboard, inline=inline, one_time=one_time, personal=personal)
        if new_kb is not None:
            data['keyboard'] = dumps(new_kb)

        for kw in kwargs:
            data[kw] = kwargs[kw]

        await self.TempData.bot(method='messages.send', params=data)

    async def return_menu(self, text='🤖 Вы были возвращены в главное меню.', keyboard=[], inline=False,
                          one_time=False, **kwargs):
        data = {'peer_id': self.uid, 'random_id': random.randint(
            1, 10000000), 'message': text}

        if menu_bot is not None:
            new_kb = create_keyboard(
                kb=keyboard, inline=inline, one_time=one_time)
        else:
            new_kb = create_keyboard(
                kb=menu_bot, inline=inline, one_time=one_time)

        if new_kb is not None:
            data['keyboard'] = dumps(new_kb)

        for kw in kwargs:
            data[kw] = kwargs[kw]

        await self.TempData.bot(method='messages.send', params=data)

    def mention(self):
        if self.is_mention is True:
            return f'[id{self.uid}|{self.nickname}]'
        else:
            return self.nickname

    def admin_mention(self):
        return f'[id{self.uid}|{self.status} ({self.admin_lvl} ур.)]'

    def gender_word(self, male, female, unknown):
        if self.gender == 1:
            return male
        elif self.gender == 2:
            return female
        else:
            return unknown

    def __str__(self):
        return f'{self.id} | {self.uid} | {self.nickname} '


class Chats(models.Model):
    class TempData:
        bot = None

    uid = models.TextField(default='', null=True,
                           blank=True, help_text='ID беседы')
    title = models.TextField(default='', help_text='название беседы')
    activation = models.BooleanField(default=False, help_text='Активация')
    malling = models.BooleanField(default=True, help_text='Рассылка')

    prize = models.BooleanField(default=False, help_text='Получение приза')

    keyboard = models.BooleanField(default=False)
    games = models.BooleanField(default=True, help_text='Игры')
    rules = models.TextField(default='', null=True,
                             blank=True, help_text='Правила')
    greeting = models.TextField(
        default='', null=True, blank=True, help_text='Приветствие')

    messages = models.BigIntegerField(default=0, help_text='сообщения беседы')
    type = models.BooleanField(default=False, help_text='админ беседа')

    class Meta:
        verbose_name = "Беседы"
        verbose_name_plural = "Беседы"
        ordering = ("id", "uid", "activation", "malling", "prize",
                    "keyboard", "games", "rules", "greeting", "messages", "type")

    async def reply(self, text=None, keyboard=None, inline=False, one_time=False, **kwargs):
        data = {'peer_id': self.uid, 'random_id': random.randint(
            1, 10000000), 'message': text}
        new_kb = create_keyboard(kb=keyboard, inline=inline, one_time=one_time)
        if new_kb is not None:
            data['keyboard'] = dumps(new_kb)

        for kw in kwargs:
            data[kw] = kwargs[kw]

        await self.TempData.bot(method='messages.send', params=data)

    async def return_menu(self, text='🤖 Вы были возвращены в главное меню.', **kwargs):
        data = {'peer_id': self.uid, 'random_id': random.randint(
            1, 10000000), 'message': text}

        if self.keyboard is False:
            keyboard = menu_bot
        else:
            keyboard = []

        new_kb = create_keyboard(kb=keyboard, inline=False, one_time=False)
        if new_kb is not None:
            data['keyboard'] = dumps(new_kb)

        for kw in kwargs:
            data[kw] = kwargs[kw]

        await self.TempData.bot(method='messages.send', params=data)

    def __str__(self):
        return f'{self.id} | {self.uid} | {self.activation} | {self.malling} | {self.keyboard} | {self.games}' \
               f' | {self.rules} | {self.greeting}'


class ChatsUser(models.Model):
    class TempData:
        bot = None

    chat = models.ForeignKey(Chats, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='chat_ChatsUser', help_text='Беседа')
    user = models.ForeignKey(Account, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='user_ChatsUser', help_text='Пользователь')

    is_moder = models.BooleanField(default=False, help_text='Модератор')
    is_admin = models.BooleanField(default=False, help_text='Админстратор')
    is_owner = models.BooleanField(default=False, help_text='Основатель')

    mention = models.BooleanField(default=True, help_text='Упоминание')
    ban_time = models.DateTimeField(
        help_text='Время бана', default=datetime.now)
    mute_time = models.DateTimeField(
        help_text='Время мута', default=datetime.now)
    warns = models.IntegerField(default=0, help_text='Кол-во варнов')

    async def reply(self, text=None, keyboard=None, inline=False, one_time=False, **kwargs):
        data = {'peer_id': self.chat.uid, 'random_id': random.randint(
            1, 10000000), 'message': text}
        new_kb = create_keyboard(kb=keyboard, inline=inline, one_time=one_time)
        if new_kb is not None:
            data['keyboard'] = dumps(new_kb)

        for kw in kwargs:
            data[kw] = kwargs[kw]

        await self.TempData.bot(method='messages.send', params=data)

    class Meta:
        verbose_name = "Беседа (Пользователи)"
        verbose_name_plural = "Беседа (Пользователи)"
        ordering = ("id", "chat", "user", "is_moder", "is_admin", "is_owner", "mention", "ban_time", "mute_time",
                    "warns")

    def __str__(self):
        return f'{self.id} | {self.chat} | {self.user} | {self.is_moder} | {self.is_admin} | {self.is_owner}' \
               f' | {self.mention} | {self.ban_time} | {self.mute_time} | {self.warns}'

class WordFilters(models.Model):
    word = models.TextField(default='', null=True,
                            blank=True, help_text='Слово')
    chat = models.ForeignKey(Chats, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='chat_WordFilters', help_text='Беседа')

    class Meta:
        verbose_name = "Фильтр слов (Беседы)"
        verbose_name_plural = "Фильтр слов (Беседы)"
        ordering = ("id", "word", "chat")

    def __str__(self):
        return f'{self.id} | {self.word} | {self.chat}'

