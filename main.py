import telebot
from telebot import types
import datetime
from googletrans import Translator
import os

token = os.getenv("TOKEN")
bot = telebot.TeleBot(token)
print(token)

# struct - nickname; data; price; type; product;
data = []
buy = [0, 1, 2, 3, 4]
translator = Translator()


def format_data_to_str(data):
    if len(data) == 0:
        return 'data is empty'
    return '\n'.join([' '.join(map(str, i)) for i in data])


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Buy")
    btn2 = types.KeyboardButton("Result")
    btn3 = types.KeyboardButton("Remove_last")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     text="Hi, {0.first_name}! I'm a bot for control your expenses".format(message.from_user),
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Buy":
        bot.register_next_step_handler(message, get_price)  # next step - get_price
        bot.send_message(message.from_user.id, "Write a price")
    elif message.text == "Result":
        bot.send_message(message.from_user.id, format_data_to_str(data))
    elif message.text == 'Remove_last':
        if len(data) != 0:
            bot.register_next_step_handler(message, delete_last_data)
            bot.send_message(message.from_user.id, 'Are you sure? If yes write "Yes"')
        else:
            bot.send_message(message.from_user.id, 'Statistic is empty')
    else:
        bot.send_message(message.from_user.id, 'write "Buy" or "Result"')


def delete_last_data(message):
    global data
    if message.text == 'Yes':
        del data[-1]
        bot.send_message(message.from_user.id, format_data_to_str(data))


def get_price(message):
    global buy
    try:
        price = int(message.text)
        buy[2] = price
        bot.send_message(message.from_user.id, "Write a type")
        bot.register_next_step_handler(message, get_type)
    except Exception as s:
        bot.send_message(message.from_user.id, 'Ошибка ввода: Введите число')
        bot.register_next_step_handler(message, get_price)


def get_type(message):
    global buy

    try:
        type = translator.translate(message.text).text
        buy[3] = type
        bot.send_message(message.from_user.id, "Write a product")
        bot.register_next_step_handler(message, get_product)
    except Exception as s:
        bot.send_message(message.from_user.id, 'Ошибка ввода: Повторите попытку')
        bot.register_next_step_handler(message, get_type)


def get_product(message):
    global buy, data
    try:
        product = translator.translate(message.text).text
        buy[4] = product
        buy[1] = datetime.datetime.today().strftime('%x %X')
        buy[0] = message.from_user.username
        data.append(buy.copy())
        bot.send_message(message.from_user.id, f"I'm wrote this data: {format_data_to_str([data[-1]])}")
    except Exception as s:
        bot.send_message(message.from_user.id, 'Ошибка ввода: Повторите попытку')
        bot.register_next_step_handler(message, get_product)


bot.polling(none_stop=True, interval=0)
