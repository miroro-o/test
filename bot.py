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

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Нажмите /show_all_dishes для того, чтобы увидеть все блюда\n'
                                    'Нажмите /choose_by_price для того, чтобы выбрать блюдо по ценовой категории\n'
                                    'Нажмите /choose_by_cooker для того, чтобы выбрать блюдо по категории\n')

async def show_all_dishes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    dishes = get_data()
    if dishes:
        await update.message.reply_text("Список блюд:\n")
        message = ""
        for dish in dishes:
            id, name, description, price, category, username = dish
            message += (f"номер: {id}\n"
                        f"Название: {name}\n"
                        f"Описание: {description}\n"
                        f"Цена: {price}\n"
                        f"Категория: {category}\n"
                        f"Никнейм повара: @{username}\n"
                        f"------------------\n")
            
        await update.message.reply_text(message)  # Выводим сообщение на консоль
    else:
        await update.message.reply_text("В таблице нет блюд.")
    await update.message.reply_text('Внимание!\nКаждый день список обнуляется')

async def choose_by_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Напишите макимальную цену')
    # Сохраняем состояние, чтобы ожидать ввод названия блюда
    context.user_data['awaiting_price'] = True

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Напишите название блюда, \n'
                                    'описание к нему, \n'
                                     'цену,\n'
                                     'категорию\n')
    # Сохраняем состояние, чтобы ожидать ввод названия блюда
    context.user_data['awaiting_dish_name'] = True

async def choose_by_cooker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dishes = get_data()
    if dishes:
        message = "Выберите чьи блюда будем смотреть:\n\n"
        usernames = []
        for dish in dishes:
            id, name, description, price, category, username = dish
            usernames.append(username)
        a = set(usernames)
        for inut in a:
             message += (f'Блюда {inut}\n')
        await update.message.reply_text(message)
        await update.message.reply_text("\nСкопируйте ник повара, чьи блюда хотите посмотреть"
                                        " и вставте в обратное сообщение")
        context.user_data['awaiting_user_name'] = True

    else:
        await update.message.reply_text("В таблице нет блюд.")

    
    

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Игнорируем сообщение пользователей, если у нас нет состояние ожидания
    if 'awaiting_dish_name' in context.user_data and context.user_data['awaiting_dish_name']:
        dish_name = update.message.text  # Считываем название блюда из сообщения
        username = update.message.from_user.username
        parts = dish_name.split('\n')
        if len(parts) != 4:
            await update.message.reply_text('Не могу обработать ваше сообщение. '
                                            'Нажмите /add для добавления блюда'
                                             ' или /buy, чтобы купить блюдо.')
        else:
            add_dish(parts[0], parts[1], parts[2], parts[3], username)
          # add_dish(name, description, cost, category, username)  # Добавляем блюдо в базу данных
            await update.message.reply_text(f'Вы добавили блюдо: \n{dish_name}')

        # Удаляем состояние после обработки ввода
        context.user_data['awaiting_dish_name'] = False
    elif 'awaiting_price' in context.user_data and context.user_data['awaiting_price']:
        price_vvod = update.message.text  # Считываем цену 
        if not price_vvod.replace('.' , '' , 1).isdigit() :
            await update.message.reply_text('Не могу обработать ваше сообщение :( ')
        else:
            price_vvod = float(price_vvod)
            dishes = get_data()
            if dishes:
                 message = ""
                 for dish in dishes:
                    id, name, description, price, category, username = dish
                    if price_vvod >= price:
                        message += (f"номер: {id}\n"
                        f"Название: {name}\n"
                        f"Описание: {description}\n"
                        f"Цена: {price}\n"
                        f"Категория: {category}\n"
                        f"Никнейм повара: @{username}\n"
                        f"------------------\n") 
                 if message == "":
                     await update.message.reply_text("В таблице нет блюд за такую цену")
                 else:
                     await update.message.reply_text("Список блюд:\n")
                     await update.message.reply_text(message)
            else:
                await update.message.reply_text("В таблице нет блюд.")
            
        context.user_data['awaiting_price'] = False
    elif 'awaiting_user_name' in context.user_data and context.user_data['awaiting_user_name']:
        user_name = update.message.text
        dishes = get_data()
        if dishes:
            message = ""
            for dish in dishes:
                id, name, description, price, category, username = dish
                if user_name == username:
                    message += (f"номер: {id}\n"
                                f"Название: {name}\n"
                                f"Описание: {description}\n"
                                f"Цена: {price}\n"
                                f"Категория: {category}\n"
                                f"Никнейм повара: @{username}\n"
                                f"------------------\n")
            if message == "":
                await update.message.reply_text('Не могу обработать ваше сообщение :( ')
            else:
                await update.message.reply_text("Список блюд:\n")
                await update.message.reply_text(message)
        else:
             await update.message.reply_text("В таблице нет блюд.")

        context.user_data['awaiting_user_name'] = False
    else:
        await update.message.reply_text('Не могу обработать ваше сообщение :( ')

        


def main():
    init_db()  # Инициализация базы данных

    # drop_tables()
    # clear_database()
    create_table()
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('add', add))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler('buy', buy))
    app.add_handler(CommandHandler('show_all_dishes', show_all_dishes))
    app.add_handler(CommandHandler('choose_by_price', choose_by_price))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler('choose_by_cooker', choose_by_cooker))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
