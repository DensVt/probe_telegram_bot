from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp



class FSMAdmin(StatesGroup):  # Класс с 4 пунктами, последовательных вопросов
    photo = State()  # () запускает класс!
    name = State()  # () запускает класс!
    description = State()  # () запускает класс!
    price = State()  # () запускает класс!


# базовый хендлер, который запускает нашу машину состояний
# Начало диалога загрузки нового пункта меню
@dp.message_handler(command="Загрузить", state=None)
async def cm_start(message: types.Message):
    await FSMAdmin.photo.set()
    await message.reply("Загрузи фото")

# Получаем ответ и пишем в словарь
# @dp.message_handler(content_types=["photo"], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply("Теперь введи название: ")

# Получаем второй ответ
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await FSMAdmin.next()
    await message.reply("Введи описание: ")

# Получаем третий ответ
# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text
    await FSMAdmin.next()
    return await message.reply("Теперь укажи цену: ")


# Получаем последний ответ и используем полученные данные
# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["price"] = float(message.text)

    await state.finish()  # как только прописана эта команда, бот выходит из машины состояний и полностью
                          # удаляет все что было записано


# регистрируем хендлеры(декораторы)
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=["Загрузить"], state=None)
    dp.register_message_handler(load_photo, content_types=["photo"], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)