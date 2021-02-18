import telebot
from telebot import types
import os
from flask import Flask, request
from config import *


bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)


# db = mysql.connector.connect(
#         host=os.getenv('myhost'),
#         user=os.getenv('myuser'),
#         passwd=os.getenv('mypass'),
#         port="3306",
#         database="eyefvtclr0ydnawm")
#
#
# # print(db)
# # print(db)
#
# cursor = db.cursor()

user_data = {}

class User:
    def __init__(self, question):
        self.question = question
        self.answer1 = ''
        self.answer2 = ''
        self.answer3 = ''
        self.answer4 = ''


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Привет, мой друг")
    bot.send_message(message.from_user.id, text='Ты хочешь оставить свой вопрос?', reply_markup=x_keyboard())


def x_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Да', callback_data='Yes')
    keyboard.add(btn1)
    btn2 = types.InlineKeyboardButton(text='Нет', callback_data='No')
    keyboard.add(btn2)
    return keyboard


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

    if call.data == "Yes":
        ask_question(call.message)

    elif call.data == "No":
        msg = 'Пока пока'
        # Отправляем текст в Телеграм)
        bot.send_message(call.message.chat.id, msg)


@bot.message_handler(func=lambda message: True)
def ask_question(message):
    try:
        msg = bot.send_message(message.chat.id, 'Напиши здесь свой вопрос')
        bot.register_next_step_handler(msg, get_question)

    except Exception as e:
        bot.reply_to(message, 'ERROR - ask_question')


@bot.message_handler(func=lambda message: True)
def get_question(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)
        # user = user_data[user_id]

        # sql = "INSERT INTO users (QUESTION, user_id) \
        #                                   VALUES (%s, %s)"
        # val = (user.question, user_id)
        # cursor.execute(sql, val)
        # db.commit()

        # bot.send_message(message.chat.id, "Вопрос успешно зарегистрирован. Спасибо!")
        bot.send_message(-1001153348142, message.text)

        msg = bot.send_message(message.chat.id, "Введите ответ № 1")
        bot.register_next_step_handler(msg, add_answer1)

    except Exception as e:
        bot.reply_to(message, 'ERROR - get_question')


@bot.message_handler(func=lambda message: True)
def add_answer1(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.answer1 = message.text

        msg = bot.send_message(message.chat.id, "Введите ответ № 2")
        bot.register_next_step_handler(msg, add_answer2)

    except Exception as e:
        bot.reply_to(message, 'ERROR - add_answer1')

# @bot.message_handler(func=lambda message: True)
# def add_answer2(message):
#     try:
#         user_id = message.from_user.id
#         user = user_data[user_id]
#
#         user.answer2 = message.text
#
#         sql = "INSERT INTO users (user_id, QUESTION, ANSWER, ANSWER_2, ANSWER_3, ANSWER_4) \
#                                                   VALUES (%s, %s, %s, %s, %s, %s)"
#         val = (user_id, user.question, user.answer1, user.answer2, user.answer3, user.answer4)
#         cursor.execute(sql, val)
#         db.commit()
#
#         bot.send_message(message.chat.id, "Вопрос и ответы успешно зарегистрированы. Спасибо!")
#         bot.send_message(-1001153348142, message.text)
#
#     except Exception as e:
#         bot.reply_to(message, 'ERROR - add_answer2')


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "it works", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url = APP_NAME + TOKEN)
    return "it worksssssssss", 200


if __name__ == '__main__':
    server.debug = True
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

















# import telebot
# from flask import Flask, request
# from config import *
# import requests
# import schedule
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import pickle
# import time
#
# bot = telebot.TeleBot(TOKEN)
#
# server = Flask(__name__)
#
# URL = 'https://hh.ru/'
#
# class HHParser:
#
#     def __init__(self, driver):
#         self.driver = driver
#         driver.implicitly_wait(4)
#
#     def resume_wake_up(self):
#         driver.get(URL)
#         # pickle.dump(driver.get_cookies(), open("session", "wb"))
#         # time.sleep(100)
#         # print('save')
#         cookies = pickle.load(open("session", "rb"))
#         for cookie in cookies:
#             driver.add_cookie(cookie)
#         driver.refresh()
#
#         driver.find_element_by_class_name("HH-Supernova-NaviLevel2-Link").click()
#
#         resumeUp = driver.find_elements_by_class_name("applicant-resumes-update-button")
#         for resume in resumeUp:
#             try:
#                 resume.click()
#             except:
#                 pass
#
#
# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     bot.send_message(message.from_user.id, "Bot works")
#
# def resume_schedule():
#     main()
#     parser = HHParser(driver)
#     parser.resume_wake_up()
#     bot.send_message(-1001364950026, "Resumes were updated")
#
#
# #
# # def photo_schedule():
# #     main()
# #     parser = PictureParser(driver)
# #     link = parser.get_link()
# #     quit()
# #     bot.send_photo(-1001364950026, photo=link)
# #
# #
# def main():
#     global driver
#     chrome_options = Options()
#     chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
#                                 'like Gecko) Chrome/85.0.4183.83 Safari/537.36')
#     # chrome_options.add_argument('headless')
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     driver = webdriver.Chrome(options=chrome_options)
#
#
# schedule.every(3).minutes.do(resume_schedule)
#
# while True:
#     schedule.run_pending()
#
#
# @server.route('/' + TOKEN, methods=['POST'])
# def getMessage():
#     bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#     return "it works", 200
#
# @server.route("/")
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url = APP_NAME + TOKEN)
#     return "it worksssssssss", 200
#
#
# if __name__ == '__main__':
#     server.debug = True
#     server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
