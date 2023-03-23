from app.bot.assets import Command, Payload, Callback


commands, payloads, callbacks = ([], [], [],)


def message(**kwargs):
    def with_args(handler):
        if kwargs.keys() & {'name'}:
            if not isinstance(kwargs['name'], list):
                kwargs['name'] = [kwargs['name']]
            for cmd in kwargs['name']:
                commands.append(Command(name=cmd, handler=handler,
                                        admin=(kwargs['admin'] if 'admin' in kwargs else False),
                                        with_args=(kwargs['with_args'] if 'with_args' in kwargs else False),
                                        game_chat=(kwargs['game_chat'] if 'game_chat' in kwargs else False),
                                        only_chat=(kwargs['only_chat'] if 'only_chat' in kwargs else False),
                                        chat_activation=(
                                            kwargs['chat_activation'] if 'chat_activation' in kwargs else False),
                                        is_moder=(kwargs['is_moder'] if 'is_moder' in kwargs else False),
                                        is_admin=(kwargs['is_admin'] if 'is_admin' in kwargs else False),
                                        is_owner=(kwargs['is_owner'] if 'is_owner' in kwargs else False)))
        else:
            return False
    return with_args


def payload(**kwargs):
    def with_args(handler):
        if kwargs.keys() & {'name'}:
            if not isinstance(kwargs['name'], list):
                kwargs['name'] = [kwargs['name']]
            for cmd in kwargs['name']:
                payloads.append(Payload(name=cmd, handler=handler,
                                        admin=(kwargs['admin'] if 'admin' in kwargs else False),
                                        with_args=(kwargs['with_args'] if 'with_args' in kwargs else False),
                                        game_chat=(kwargs['game_chat'] if 'game_chat' in kwargs else False),
                                        only_chat=(kwargs['only_chat'] if 'only_chat' in kwargs else False),
                                        chat_activation=(
                                            kwargs['chat_activation'] if 'chat_activation' in kwargs else False),
                                        is_moder=(kwargs['is_moder'] if 'is_moder' in kwargs else False),
                                        is_admin=(kwargs['is_admin'] if 'is_admin' in kwargs else False),
                                        is_owner=(kwargs['is_owner'] if 'is_owner' in kwargs else False)))
        else:
            return False
    return with_args


def callback(**kwargs):
    def with_args(handler):
        if kwargs.keys() & {'name'}:
            if not isinstance(kwargs['name'], list):
                kwargs['name'] = [kwargs['name']]
            for cmd in kwargs['name']:
                callback.append(Callback(name=cmd, handler=handler,
                    with_args=(kwargs['with_args'] if 'with_args' in kwargs else False)))
        else:
            return False
    return with_args