def digit(num):
    num = int(num)
    return '{:,}'.format(num).replace(',', '.')


def create_keyboard(kb=None, one_time=False, inline=False, personal: str = None):
    if kb is not None:
        if inline is False:
            one_time = one_time
        else:
            one_time = False

        data = {
                "one_time": one_time,
                "inline": inline,
                "buttons": []
            }

        for button in kb:
            bt = []
            for act in button:
                
                if personal:
                    act["payload"]["payload"] += " "+personal
                    act["payload"]["personal"] = True
                else:
                    act["payload"]["personal"] = False
                bt_color = act.get("color", None)
                if bt_color is not None:
                    act.pop("color")

                new_data = {"action": act}
                if bt_color is not None:
                    new_data["color"] = bt_color

                bt.append(new_data)

            data["buttons"].append(bt)
            

        return data
    else:
        return None
    

async def message_send(text, user, chat_user, **kwargs):
    data = {}
    for kw in kwargs:
        data[kw] = kwargs[kw]

    if chat_user is not None:
        await chat_user.reply(text=text)
    else:
        await user.reply(text=text)