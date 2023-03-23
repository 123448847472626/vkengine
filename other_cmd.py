from app.models import Account, WordFilters


digit = lambda num: '{:,}'.format(num).replace(',', '.')



async def number_to_emoji(num):
    return str(num).replace('0', '0️⃣').replace('1', '1️⃣').replace('2', '2️⃣').replace('3', '3️⃣').replace('4', '4️⃣').replace('5', '5️⃣').replace('6', '6️⃣').replace('7', '7️⃣').replace('8', '8️⃣').replace('9', '9️⃣').replace('10', '🔟')


def digit_convert(value, currency):
    currency = {'bd': currency}
    if value in ['все', 'всё', 'all']:
        value = str(int(currency['bd']))
    else:
        value = value.replace('к', '000')
        value = value.replace('k', '000')
    return int(value) if value.isdigit() else None


# def datetime_convert(value):
#     days, seconds = value.days, value.seconds
#     return f'{days * 24 + seconds // 3600}:{(seconds % 3600) // 60}:{seconds % 60}'

def convert_timedelta(dt, type):
    if type == 'time':
        return f'{dt.seconds//3600}:{(dt.seconds//60)%60}:{dt.seconds%60}'
    elif type == 'datetime':
        return f'{dt.days}:{dt.seconds//3600}:{(dt.seconds//60)%60}:{dt.seconds%60}'

# def creating_menu_pages(pay_m, selector=5):
#     result = []

#     def append(elem, id):
#         result[id].append(elem)

#     for i in range(0, pay_m.__len__() % selector + len(pay_m)):
#         result.append(list())
#         for j in range(i * selector, (i + 1) * selector):
#             try:
#                 append(pay_m[j], i)
#             except:
#                 pass

#     result = list(filter(None, result))
#     return result

def creating_menu_pages(list_items, separator=5):
    objects_list = []
    for item in list_items:
        if len(objects_list) == separator:
            yield objects_list
            objects_list = []
        objects_list.append(item)
    yield objects_list

async def get_user_info(bot, member_id, name_case='Nom'):
    send_api = await bot.api(method='users.get', params={'user_ids': member_id, 'name_case': name_case})
    load_response = send_api.get('response', None)
    if load_response is not None:
        return load_response[0]
    else:
        load_error = send_api.get('error', None)
        if load_error is not None:
            return None
        else:
            return None


async def remove_member(bot, chat, remove_id):
    send_api = await bot.api(method='messages.removeChatUser',
                             params={'chat_id': int(chat.uid) - 2000000000, 'user_id': remove_id})

    load_response = send_api.get('response', None)
    if load_response is not None:
        return [True]
    else:
        load_error = send_api.get('error', None)
        if load_error is not None:
            error_code = send_api['error']['error_code']
            return [False, error_code]
        else:
            return [False, 0]


async def remove_message(bot, chat, message_id, type='1', peer_id=None):
    if type == '1':
        send_api = await bot.api(method='messages.delete',
                                params={'peer_id': int(chat.uid),
                                        'conversation_message_ids': message_id,
                                        'delete_for_all': 1})
    else:
        send_api = await bot.api(method='messages.delete',
                                params={'peer_id': peer_id,
                                        'conversation_message_ids': message_id,
                                        'delete_for_all': 1})

    load_response = send_api.get('response', None)
    if load_response is not None:
        return [True]
    else:
        load_error = send_api.get('error', None)
        if load_error is not None:
            error_code = send_api['error']['error_code']
            return [False, error_code]
        else:
            return [False, 0]

async def get_chat_name(bot, peer_id):
    send_api = await bot.api(method='messages.getConversationsById',
                      params={'peer_ids': peer_id})
    
    load_response = send_api.get('response', None)
    if load_response is not None:
        print(load_response)
        return load_response['items']
    else:
        load_error = send_api.get('error', None)
        if load_error is not None:
            error_code = send_api['error']['error_code']
            return [False, error_code]
        else:
            return [False, 0]


async def remove_vk_link(type, link):
    if type == 1:
        link = link.replace('https://vk.com/id', '')
        link = link.replace('http://vk.com/id', '')
        link = link.replace('vk.com/id', '')
        link = link.replace('https://vk.com/', '')
        link = link.replace('http://vk.com/', '')
        link = link.replace('vk.com/', '')
        link = link.replace('@', '')
        link = link.replace('*', '')
        return link
    else:
        link = link.replace('[id', '').partition('|')[0]
        return link


async def check_filter(chat, bot, args, chat_user):
    if chat is not None:
        if chat_user.is_moder is False:
            if chat_user.is_admin is False:
                if chat_user.is_owner is False:
                    if WordFilters.objects.filter(chat=chat, word__in=args).count() > 0:
                        get_remove_member = await remove_member(bot=bot, chat=chat, remove_id=chat_user.user.uid)
                        if get_remove_member[0]:
                            await chat.reply(f'ℹ [id{chat_user.user.uid}|Пользователь] написал слово из запрещённого списка и был исключён из этой беседы!')
                        return False
                    else:
                        return True
                else:
                    return True
            else:
                return True
        else:
            return True
    else:
        return True


async def hello_message(chat, chat_user, GROUP_ID, BOT_NAME):
    if chat.greeting == '':
        text = f'👋🏻 Привет всем участникам беседы! Я — игровой бот [public{GROUP_ID}|{BOT_NAME}].\n'
    else:
        text = chat.greeting

    keyboard = [[{"label": "🗂 Помощь", "type": "text", "color": "secondary", "payload": {"payload": "help"}}]]
    await chat_user.reply(text=text, keyboard=keyboard, inline=True)


async def declin(number, word1, word2, word3):
    number = str(number)
    if number[-1] == '1':
        return word1
    elif number[-1] in ['2', '3', '4']:
        return word2
    else:
        return word3

def initial(currency):
    try:
        return int(currency)
    except:
        return None