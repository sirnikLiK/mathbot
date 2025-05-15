from pyexpat.errors import messages

import math
import conf
import telebot
import re
from uuid import uuid4
from telebot import types

import latex_ocr

import sys

sys.set_int_max_str_digits(0)

import sympy as sp
from sympy import *

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
        """
        /start - нажмите, если хотите запустить бот\n/about - нажмите, если хотите узнать информацию о боте\n/calc - нажмите, если хотите вычислить выражение\n/equat - нажмите, если хотите решить уравнение\n/log - нажмите, если хотите вычислить логарифм
        """
    )


@bot.message_handler(commands=['about'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Этот бот поможет решить вам различные выражения и уравнения. "
        "Чтобы узнать команды введите команду '/help'."
    )


@bot.message_handler(commands=['log'])
def log_text(message):
    msg = bot.send_message(
        message.chat.id,
        "Введите выражение в формате log(n, base) base - основание логарифма:"
    )
    bot.register_next_step_handler(msg, log_new)


def log_new(message):
    expr = message.text
    result = eval(f"__import__('math').{expr}")
    try:
        bot.reply_to(message, f'🔢Решение: {result}')
    except Exception as e:
        bot.reply_to(message,
                     f'⚠️ Ошибка: Введите логарифм в формате: log(n, base), log10(n), log2(n)')


@bot.message_handler(commands=['calc'])
def text(message):
    msg = bot.send_message(
        message.chat.id,
        "Введите выражение:"
    )
    bot.register_next_step_handler(msg, after_text)


def after_text(message):
    expr = message.text.replace(" ", "").replace(",", ".")

    if not re.match(r"^[\d+\-*/().^√]*$", expr):
        print([expr])
        bot.reply_to(message, "⚠️ Ошибка: Используйте только цифры и операторы + - * / ^ ( )")
        return

    try:
        expr = expr.replace("^", "**").replace("√", "math.sqrt")

        result = eval(f"__import__('math').{expr}" if "sqrt" in expr else expr)

        bot.reply_to(message,
                     f"🔢 Результат: {message.text} = {round(result, 4) if isinstance(result, float) else result}")

    except ZeroDivisionError:
        bot.reply_to(message, "⛔️ Ошибка: Деление на ноль!")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка вычисления: {str(e)}")


def solve_equation(equation):
    x = sp.symbols('x')
    lhs, rhs = equation.split('=')
    lhs = sp.sympify(lhs)
    rhs = sp.sympify(rhs)
    solution = sp.solve(lhs - rhs, cubics=False)
    return solution


@bot.message_handler(commands=['equat'])
def the_equatation_message(message):
    msg = bot.send_message(
        message.chat.id,
        "Введите уравнение в формате 'левая_часть = правая_часть' (например, '2*x + 3 = 7'):"
    )
    bot.register_next_step_handler(msg, the_equatation)


def the_equatation(message):
    equation = message.text
    try:
        solution = solve_equation(equation)
        bot.reply_to(message, f'🔢Решение: {', '.join(map(str, solution))}')
    except Exception as e:
        bot.reply_to(message,
                     f'⚠️ Ошибка: Введите уравнение в формате "левая_часть = правая_часть" (например, "2*x + 3 = 7")')




@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id,
                     "Введите команду /help, чтобы узнать команды"
                     )


bot.polling(none_stop=True)
