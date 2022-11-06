from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot  # ОТКЛЮЧИТЬ / ПОДКЛЮЧИТЬ ПРОВЕРКУ НА АДМИНИСТРАТОРА !!!
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keybords import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ID = None  # ОТКЛЮЧИТЬ / ПОДКЛЮЧИТЬ ПРОВЕРКУ НА АДМИНИСТРАТОРА !!!


class FSMAdmin(StatesGroup):  # Класс с 4 пунктами, последовательных вопросов
    photo = State()  # () запускает класс!
    name = State()  # () запускает класс!
    description = State()  # () запускает класс!
    price = State()  # () запускает класс!


#  Получаем ID текущего модератора
# @dp.message_handler(commands=["moderator"], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id  # проверка на администратора
    await bot.send_message(message.from_user.id, "Что конкретно нужно?", reply_markup=admin_kb.button_case_admin)
    await message.delete()


# ОТКЛЮЧИТЬ / ПОДКЛЮЧИТЬ ПРОВЕРКУ НА АДМИНИСТРАТОРА !!!


# базовый хендлер, который запускает нашу машину состояний
# Начало диалога загрузки нового пункта меню
# @dp.message_handler(commands="Загрузить", state=None)   # декоратор
async def cm_start(message: types.Message):
    if message.from_user.id == ID:  # ОТКЛЮЧИТЬ / ПОДКЛЮЧИТЬ ПРОВЕРКУ НА АДМИНИСТРАТОРА !!!
        await FSMAdmin.photo.set()
        await message.reply("Загрузи фото")


# в любой машине состояния, должна быть команда отмены (если юзер передумал вводить строку дальше)
# вывод бота из состояния машины состояния
# Выход из состояния

# @dp.message_handler(state="*", commands="отмена")
# @dp.message_handler(Text(equals="отмена", ignore_case=True), state="*") # для "отмены" без команды "/"
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:  # ОТКЛЮЧИТЬ / ПОДКЛЮЧИТЬ ПРОВЕРКУ НА АДМИНИСТРАТОРА !!!
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply("OK")


# Получаем ответ и пишем в словарь
# @dp.message_handler(content_types=["photo"], state=FSMAdmin.photo)    # декоратор
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:  # ОТКЛЮЧИТЬ / ПОДКЛЮЧИТЬ ПРОВЕРКУ НА АДМИНИСТРАТОРА !!!
        async with state.proxy() as data:
            data["photo"] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply("Теперь введи название: ")


# Получаем второй ответ
# @dp.message_handler(state=FSMAdmin.name)    # декоратор
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:  # ОТКЛЮЧИТЬ / ПОДКЛЮЧИТЬ ПРОВЕРКУ НА АДМИНИСТРАТОРА !!!
        async with state.proxy() as data:
            data["name"] = message.text
        await FSMAdmin.next()
        await message.reply("Введи описание: ")


# Получаем третий ответ
# @dp.message_handler(state=FSMAdmin.description)    # декоратор
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:  # ОТКЛЮЧИТЬ / ПОДКЛЮЧИТЬ ПРОВЕРКУ НА АДМИНИСТРАТОРА !!!
        async with state.proxy() as data:
            data["description"] = message.text
        await FSMAdmin.next()
        return await message.reply("Теперь укажи цену: ")


# Получаем последний ответ и используем полученные данные
# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:  # ОТКЛЮЧИТЬ / ПОДКЛЮЧИТЬ ПРОВЕРКУ НА АДМИНИСТРАТОРА !!!
        async with state.proxy() as data:
            data["price"] = float(message.text)

        await sqlite_db.sql_add_command(state)  # запись в бд
        await state.finish()  # как только прописана эта команда, бот выходит из машины состояний и полностью
    # удаляет все что было записано

@dp.callback_query_handler(lambda x: x.data and x.data.startswith("del")) # если событие начинается с дел пробел
async def del_callback_run(callback_query: types.CallbackQuery): # callback_query(можно назвать как угодно)
    await sqlite_db.sql_delete_command(callback_query.data.replace("del ", ""))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)
    # запрос выполнен, отправка админу о том что данная пицца удалена

# @dp.message_handler(commands="Удалить")
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f"{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}")
            await bot.send_message(message.from_user.id, text="^^^", reply_markup=InlineKeyboardMarkup().
                                   add(InlineKeyboardButton(f"Удалить {ret[1]}", callback_data=f"del {ret[1]}")))


# регистрируем хендлеры(декораторы)
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=["Загрузить"], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands="отмена")
    dp.register_message_handler(cancel_handler, Text(equals="отмена", ignore_case=True), state="*")
    # для "отмены" без команды "/"
    dp.register_message_handler(load_photo, content_types=["photo"], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_changes_command, commands=["moderator"], is_chat_admin=True)
    # ОТКЛЮЧИТЬ / ПОДКЛЮЧИТЬ ПРОВЕРКУ НА АДМИНИСТРАТОРА !!!
    dp.register_message_handler(delete_item, commands=["Удалить"], state=None)
    dp.register_message_handler(del_callback_run, )

