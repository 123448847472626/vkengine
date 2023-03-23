from app.bot import handler


@handler.message(name='привет')
async def _(message, args, bot, user, chat, chat_user):
    await user.reply(f'{user.mention()}, привет!')
