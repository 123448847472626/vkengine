from . import handler
from engine import console
from .vk.LongPoll import VK
from django.conf import settings
import os
import importlib
import re
import asyncio
import json
from .app_functions import register_user, register_chat, register_chat_user
from app.models import Account, Chats, ChatsUser
from other_cmd import remove_member, hello_message, check_filter, remove_message, remove_vk_link
from app.bot.vk.RequestsToVK import post as vkPost


class VkBot:
	def __init__(self):
		os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

		self.loop = asyncio.get_event_loop()
		self.loop.run_until_complete(asyncio.wait([
			self.start(),
		]))

	async def start(self):
		await console.log('Инициализация VK...')
		self.vk = VK()

		await self.read_handlers()

		Chats.TempData.bot = self.vk.api
		Account.TempData.bot = self.vk.api
		ChatsUser.TempData.bot = self.vk.api

		@self.vk.responseHandler()
		async def responseHandler(update):
			if update['type'] == 'message_new' or update['type'] == 'message_event':
				if update['type'] == 'message_event':
					message_event = {
								'from_id': update['object']['user_id'],
								'id': update['object'].get('conversation_message_id'),
								'out': 0,
								'attachments': [],
								'conversation_message_id': update['object']['conversation_message_id'],
								'fwd_messages': [],
								'important': False,
								'is_hidden': False,
								'payload': update['object']['payload'],
								'peer_id': update['object']['peer_id'],
								'random_id': 0,
								'text': ' ',
								'event_id': update['object']['event_id'],
								'type': 'callback'
							}
				else:
					event = update['object']['message']

				if event['from_id'] > 0:
					user = await register_user(event['from_id'])

				action = event.get('action', None)

				if action is None:
						get_payload = event.get('payload', None)
						payload_command = None

						if get_payload is not None and get_payload != '':
							if type(event['payload']) == dict:
								payload_command_json = event['payload']
							else:
								payload_command_json = json.loads(event['payload'])

							if type(payload_command) != str:
								payload_command = payload_command_json.get('command', None)
								if payload_command is None:
									payload_command = payload_command_json.get('payload', None)

						processed_name = event['text'].lower().strip()
						processed_name = processed_name.replace(
							f'[club{settings.GROUP_ID}|{processed_name[processed_name.find("|") + 1: processed_name.find("]")]}]', '').strip()
						processed_name = re.sub(
							r'^[^а-яА-ЯёЁ]\s', '', processed_name)
						args = re.split(r'\s+', processed_name)
						error_message = f'{user.mention()}, произошла ошибка!'
						no_command = f'{user.mention()}, команда не найдена!'

						if event['peer_id'] > 2000000000:
							chat = await register_chat(event)
							chat_user = await register_chat_user(user, chat)
       
						else:
							chat, chat_user = None, None

							if user.wrote_personal is False:
								user.wrote_personal = True
								user.save()

							if user.ban is False:
								if payload_command is None:
									get_check_filter = await check_filter(chat=chat, bot=self.vk,
																		  args=args, chat_user=chat_user)
         
									if get_check_filter:
										for command in handler.commands:
											if (not command.with_args and command.name in ['', processed_name]) or (command.with_args and command.name in ['', args[0], " ".join(x for x in args[0:len(command.name.split())]) if len(args) >= len(command.name.split()) else ""]):
												if not await command.handle(event, args, self.vk, user, chat, chat_user):
													await user.reply(error_message)
												break
											else:
												if chat is None:
													await user.reply(no_cmd, keyboard=[[{"label": "🗂 Помощь", "type": "text", "color": "secondary", "payload": {"payload": "help"}}]], inline=True)
									else:
										await remove_member(bot=self.vk, chat=chat, remove_id=chat_user.user.uid)
								else:
									payload_command = re.split(
										r'\s+', payload_command)
									for payload in handler.payloads:
										if payload.name == payload_command[0]:
											if event.get("type") == 'callback':
												if event['payload']['personal'] and user.uid != payload_command[-1]:
													await vkPost(method='messages.sendMessageEventAnswer', params = {
														'access_token': settings.BOT_TOKEN,
														'event_id': event['event_id'],
														'user_id': event['from_id'],
														'peer_id': event['peer_id'],
														'event_data': json.dumps({'type': 'show_snackbar','text': '❌ Ты не можешь использовать эту кнопку т.к она тебе не принадлежит'}),
														'v': '5.131'
													})
													break
											if not await payload.handle(event, payload_command, self.vk, user, chat, chat_user):
												await user.reply(err_msg)
											if event.get("type") == 'callback':
												await vkPost(method='messages.sendMessageEventAnswer', params = {
															'access_token': settings.BOT_TOKEN,
															'event_id': event['event_id'],
															'user_id': event['from_id'],
															'peer_id': event['peer_id'],
															'v': '5.131'
														})
											break
									else:
										if chat is None:
											await user.reply(no_cmd, keyboard=[[{"label": "🗂 Помощь", "type": "text", "color": "secondary", "payload": {"payload": "help"}}]], inline=True)
				else:
					if action['type'] == 'chat_invite_user':
						GROUP_ID = os.environ['GROUP_ID']
						BOT_NAME = os.environ['BOT_NAME']
						event = update['object']['message']

						chat = await register_chat(event=event)

						if action['member_id'] < 0:
							if action['member_id'] == -int(GROUP_ID):
								await chat.reply(
									f'👋🏻 Привет всем участникам беседы.')
						else:
							await chat.reply(await chat_user_add(uid=action['member_id']), keyboard=user_join_group_keyboard, inline=True)
							member_user = await register_user(user_id=action['member_id'])
							chat = await register_chat(event=event)

			elif update['type'] == 'group_join':
				event = update['object']
				acc_data = await register_user(event['user_id'])

		await self.vk.LongPoll()
  
	async def read_handlers(self):
		PLATFORM_VERSION = "0.1"
		await console.log(f'Запуск VkEngine (v.{PLATFORM_VERSION})...')
		await console.log('Инициализация команд бота...')

		for root, dirs, files in os.walk('app/bot/commands'):
			check_extension = filter(lambda x: x.endswith('.py'), files)
			for command in check_extension:
				path = os.path.join(root, command)
				spec = importlib.util.spec_from_file_location(
					command, os.path.abspath(path))
				module = importlib.util.module_from_spec(spec)
				spec.loader.exec_module(module)

		await console.log('Бот готов к работе!')