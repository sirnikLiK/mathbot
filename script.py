import conf
import telebot

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
        'Этот бот поможет решить вам уравнения.'
    )
bot.polling(none_stop=True)
