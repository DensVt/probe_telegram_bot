from aiogram import types, Dispatcher
# from create_bot import dp
import json, string


# @dp.message_handler()
async def echo_send(message: types.Message):
    if {elem.lower().translate(str.maketrans("", "", string.punctuation)) for elem in message.text.split(" ")} \
            .intersection(set(json.load(open("cenzura.json")))) != set():
        await message.reply("Маты запрещены")
        await message.delete()


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
