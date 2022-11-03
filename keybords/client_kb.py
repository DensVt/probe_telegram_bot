from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove  # классы отвечают за кнопки

b1 = KeyboardButton("/Режим_работы") # отображение кнопок и отправка боту
b2 = KeyboardButton("/Расположение") # отображение кнопок и отправка боту
b3 = KeyboardButton("/Меню")         # отображение кнопок и отправка боту

# Кнопки исключение, добавляют не то что в них написано
# b4 = KeyboardButton("Поделиться номером", request_contact=True) # 2 аргумент в приоритете
# b5 = KeyboardButton("Отправить где я", request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) # замена клавиатуры стандартной на нашу
# one_time_keyboard=True спрятать клаву после выбора пользователя, однако, пользователь может ее открыть

# kb_client = ReplyKeyboardMarkup(resize_keyboard=True) Это при удаление клавы

# kb_client.add(b1).add(b2).add(b3) # добавление кнопок с новой строки (это первый метод, их всего 3)
# kb_client.add(b1).add(b2).insert(b3)  # метод 2 (добавление кнопки прямо в строку)
# kb_client.row(b1, b2, b3) # метод 3 (добавление всех кнопок в строку)

kb_client.add(b3).row(b1, b2) #.row(b4, b5)