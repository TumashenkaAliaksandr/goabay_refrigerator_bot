from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Создаем клавиатуру с кнопками
buttons_menu = ReplyKeyboardMarkup(resize_keyboard=True)
buttons_menu.add(KeyboardButton("Получить ссылки"))
buttons_menu.add(KeyboardButton("Посмотреть задания"))
