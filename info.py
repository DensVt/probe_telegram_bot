# создание телеграм бота
#
# поиск -> BotFather
# создать -> newbot
# имя -> Probe_Pizza_mix
# имя бота -> probe_pizza_bot
# закрыть токен -> setprivacy
# Current status is: ENABLED  -> Disable
#
#
# создать бат файл
# имя -> bot_run.bat # отныне запуск программы с этого файла!
#
# под капотом
# @echo off
# call %~dp0telegram_bot\venv\Scripts\activate
# cd %~dp0telegram_bot
# set TOKEN=# ключ выдающийся BotFather
# python bot_telegram.py
# pause
#
#
# машина состояний
# админка с помощью телеграмма
#
# указываем хранилище, там где бот все запомнит (самое простое memory_storage -> хранит данные в оперативной памяти)
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
#
# база данных: Данные очень важны(какая-то покупка, банковские данные) -> aioredis or mongo