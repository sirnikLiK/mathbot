from pyexpat.errors import messages

import conf
import telebot
import re
from uuid import uuid4
from telebot import types

bot = telebot.TeleBot(conf.TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        'Здравствуйте! Чтобы узнать информацию о боте введите команду "/about" '
    )


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        """/start - нажмите, если хотите запустить бот,
    /about - нажмите, если хотите узнать информацию о боте, 
    /calc - нажмите, если хотите вычислить выражение"""
    )


@bot.message_handler(commands=['about'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Этот бот поможет решить вам различные выражения и уравнения. "
        "Чтобы узнать команды введите команду '/help'."
    )


@bot.message_handler(commands=['calc'])
def text(message):
    msg = bot.send_message(
        message.chat.id,
        "Введите выражение:"
    )
    bot.register_next_step_handler(msg, after_text)


def after_text(message):
    expr = message.text.replace(" ", "").replace(",", ".")

    if not re.match(r'^[\d+\-*/().^√]+$', expr):
        bot.reply_to(message, "⚠️ Ошибка: Используйте только цифры и операторы + - * / ^ √ ( )")
        return

    try:
        expr = expr.replace("^", "**").replace("√", "math.sqrt")

        result = eval(f"__import__('math').{expr}" if "sqrt" in expr else expr)

        bot.reply_to(message,
                     f"🔢 Результат: {message.text} = {round(result, 4) if isinstance(result, float) else result}")

    except ZeroDivisionError:
        bot.reply_to(message, "⛔ Ошибка: Деление на ноль!")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка вычисления: {str(e)}")


@bot.message_handler(func=lambda m: True, content_types=['photo'])
def get_broadcast_picture(message):
    file_path = bot.get_file(message.photo[0].file_id).file_path
    file = bot.download_file(file_path)
    with open("expression.png", "wb") as code:
        code.write(file)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id,
                     "Введите команду /help, чтобы узнать команды"
                     )


bot.polling(none_stop=True)
