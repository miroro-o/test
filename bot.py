import sqlite3

# Функция для инициализации базы данных
def init_db():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            status TEXT
        )
    ''')
    connection.commit()
    connection.close()
def add_user(user_id, username, first_name, last_name, status):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, username, first_name, last_name, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name, status))
    connection.commit()
    connection.close()

def get_user(user_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    connection.close()
    return user

def update_user_status(user_id, status):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE users SET status = ? WHERE user_id = ?', (status, user_id))
    connection.commit()
    connection.close()

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name

    # Добавление пользователя в базу данных
    add_user(user_id, username, first_name, last_name, 'active')

    # Создание кнопок и ответ
    button1 = KeyboardButton("Регистрация")
    button2 = KeyboardButton("Купить блюдо")
    button3 = KeyboardButton("Помощь")
    
    keyboard = ReplyKeyboardMarkup([[button1, button2], [button3]], resize_keyboard=True)
    await update.message.reply_text('Привет! Я твой помощник - povar_bot.', reply_markup=keyboard)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Обработка текстовых сообщений
    pass

def main():
    init_db()  # Инициализация базы данных
    app = ApplicationBuilder().token('7645048229:AAFjquq_04glLT0rkUUwdbWjbAMQnV5GxzM').build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == '__main__':
    main()
