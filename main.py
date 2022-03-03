import telebot
from telebot import types
import datetime
from googletrans import Translator

bot = telebot.TeleBot('5116797216:AAHgRkyxPXwYWy75uNCAo3626-YaokDNUEE')

# struct - data; price; type; product;
data = []
buy = [1, 2, 3, 4]
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
    markup.add(btn1, btn2)
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
    else:
        bot.send_message(message.from_user.id, 'write "Buy" or "Result"')


def get_price(message):
    global buy
    bot.send_message(message.from_user.id, "Write a type")
    buy[1] = int(message.text)
    bot.register_next_step_handler(message, get_type)


def get_type(message):
    global buy
    bot.send_message(message.from_user.id, "Write a product")
    buy[2] = translator.translate(message.text).text
    bot.register_next_step_handler(message, get_product)


def get_product(message):
    global buy, data

    buy[3] = translator.translate(message.text).text
    buy[0] = datetime.datetime.today().strftime('%x %X')
    data.append(buy.copy())
    bot.send_message(message.from_user.id, f"I'm wrote this data: {format_data_to_str([data[-1]])}")


bot.polling(none_stop=True, interval=0)
