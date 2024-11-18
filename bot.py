from base_users import init_db, get_user, add_user, update_user_status, display_user
from config import token
from database import create_table, add_dish, drop_tables, clear_database, get_data  # Импорт необходимых функций
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    add_user(user_id, username, first_name, last_name, 'active')

    button1 = KeyboardButton("/add")
    button2 = KeyboardButton("/buy")
    button3 = KeyboardButton("/start")
    
    keyboard = ReplyKeyboardMarkup([[button3], [button2, button1]], resize_keyboard=True)
    await update.message.reply_text('Привет! Я твой помощник - povar_bot.', reply_markup=keyboard)

async def send_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    dishes = get_data()
    if dishes:
        update.message.reply_text("Список блюд:\n")
        message = ""
        for dish in dishes:
            id, name, description, price, category, username = dish
            message += (f"ID: {id}\n"
                        f"Название: {name}\n"
                        f"Описание: {description}\n"
                        f"Цена: {price}\n"
                        f"Категория: {category}\n"
                        f"Никнейм повара: @{username}\n"
                        f"------------------\n")
            
        await update.message.reply_text(message)  # Выводим сообщение на консоль
    else:
        print("В таблице нет блюд.")
    # # Формируем сообщение
    # for row in data:
    #     message = ""
    #     message += str(row) + "\n"  # Преобразуем строки в строку
    # print(message)
    # update.message.reply_text("1")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Напишите название блюда, описание к нему, цену и категорию')
    # Сохраняем состояние, чтобы ожидать ввод названия блюда
    context.user_data['awaiting_dish_name'] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Игнорируем сообщение пользователей, если у нас нет состояние ожидания
    if 'awaiting_dish_name' in context.user_data and context.user_data['awaiting_dish_name']:
        dish_name = update.message.text  # Считываем название блюда из сообщения
        username = update.message.from_user.username
        parts = dish_name.split('\n')
        if len(parts) != 4:
            await update.message.reply_text('Не могу обработать ваше сообщение. Нажмите /add для добавления блюда или /buy, чтобы купить блюдо.')
        else:
            add_dish(parts[0], parts[1], parts[2], parts[3], username)
          # add_dish(name, description, cost, category, username)  # Добавляем блюдо в базу данных
            await update.message.reply_text(f'Вы добавили блюдо: \n{dish_name}')

        # Удаляем состояние после обработки ввода
        context.user_data['awaiting_dish_name'] = False
    else:
        await update.message.reply_text('Не могу обработать ваше сообщение. Нажмите /add для добавления блюда или /buy, чтобы купить блюдо.')


def main():
    init_db()  # Инициализация базы данных

    # drop_tables()
    create_table()
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('add', add))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler('buy', send_data))
    app.run_polling()

if __name__ == '__main__':
    main()
