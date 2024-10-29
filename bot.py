import config
import telebot # pip install telebot
from telebot import types # pip install pyTelegramBotAPI
bot = telebot.TeleBot(config.token)
@bot.message_handler(commands=['go', 'start'])  # Обработка команды для старта
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item3 = types.KeyboardButton("Приложения")
    item2 = types.KeyboardButton("Мероприятия")
    item1 = types.KeyboardButton('О нас')

    markup.add(item1, item2, item3)


    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!  Я - <b>{1.first_name}</b>, бот созданный для того, чтобы вы смогли найти еду.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)
# RUN
if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except ConnectionError as e:
        print('Ошибка соединения: ', e)
    except Exception as r:
        print("Непридвиденная ошибка: ", r)
    finally:
        print("Здесь всё закончилось")