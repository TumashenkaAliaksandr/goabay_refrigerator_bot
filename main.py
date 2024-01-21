import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from decouple import config
from buttons.buttons_menu import buttons_menu
from db_connector import DatabaseConnector
import re

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получение API токена из .env файла
API_TOKEN = config('API_TOKEN')

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)

# Создание подключения к базе данных
db = DatabaseConnector('links.db')
db.create_table()

# Функция для добавления сообщения в базу данных
async def add_message_to_db(message):
    db.add_message(message)

# Асинхронная функция для добавления ссылки
async def add_link(link):
    all_links = db.get_all_links()
    print("Existing links:")
    for existing_link in all_links:
        print(existing_link)
    if link not in all_links:
        db.add_link(link)
        print(f"Added link: {link}")

# Асинхронная функция для извлечения ссылок из сохраненных сообщений
async def extract_links_from_messages():
    messages = db.get_all_messages()
    for message in messages:
        links = extract_links_from_text(message.text)
        for link in links:
            await add_link(link)

# Функция для извлечения ссылок из текста сообщения
def extract_links_from_text(text):
    pattern = r'https?://\S+'
    links = re.findall(pattern, text)
    return links

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_name = message.from_user.first_name
    text = f"👋 Hello, {user_name}! \nI'm the moderator bot for the [GoaBay](https://goabay.com/) online store! \nWelcome to GoaBay!"
    await message.answer(text, parse_mode=types.ParseMode.MARKDOWN, reply_markup=buttons_menu)

# Обработчик всех текстовых сообщений
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text_messages(message: types.Message):
    await add_message_to_db(message)
    links = extract_links_from_text(message.text)
    for link in links:
        await add_link(link)

# Запуск бота
if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    finally:
        db.close_connection()
