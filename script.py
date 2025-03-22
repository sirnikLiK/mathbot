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
        'Здравствуйте! Чтобы узнать информацию о боте введите команду "/help"'
    )

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        """Этот бот поможет решить вам уравнения.
        Чтобы бот решил вам ваше выржание введите команду """
    )

@bot.message_handler(commands=['calc'])
def calculate_expression(message):
    expr = message.text.replace(" ", "").replace(",", ".")
    
    if not re.match(r'^[\d+\-*/().^√]+$', expr):
        bot.reply_to(message, "⚠️ Ошибка: Используйте только цифры и операторы + - * / ^ √ ( )")
        return

    try:
        expr = expr.replace("^", "**").replace("√", "math.sqrt")
        
        result = eval(f"__import__('math').{expr}" if "sqrt" in expr else expr)
        
        bot.reply_to(message, f"🔢 Результат: {message.text} = {round(result, 4) if isinstance(result, float) else result}")
    
    except ZeroDivisionError:
        bot.reply_to(message, "⛔ Ошибка: Деление на ноль!")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка вычисления: {str(e)}")

bot.polling(none_stop=True)
