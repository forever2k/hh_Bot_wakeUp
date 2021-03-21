import os
from selenium import webdriver
import telebot
from flask import Flask, request
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from config import *
import pickle
import schedule
import time
import random
import requests


bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-sh-usage')

driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)
driver.implicitly_wait(4)

URL = 'https://hh.ru/'

launch = True


# @bot.message_handler(content_types=['text'])
# def lalala(message):
#     bot.send_message(227722043, message)
#     bot.send_message(227722043, message.message_id)
#     bot.send_message(227722043, message.chat.id)



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Bot hh_wakeUp works")
    # bot.send_message(message.from_user.id, message.from_user.id)


@bot.message_handler(commands=['res'])
def res(message):

    bot.send_message(message.from_user.id, "RES Bot starts to work")

    start_res()
    wake_up()

    schedule.every(250).minutes.do(wake_up)

    while launch:
        schedule.run_pending()
        time.sleep(1)


@bot.message_handler(commands=['stop'])
def stop_res(message):

    global launch
    launch = False
    bot.send_message(message.from_user.id, "STOP is activated")


def start_res():

    global launch
    launch = True


def wake_up():

    bot.send_message(227722043, "Function Wake_up starts")
    driver.get(URL)

    # hh_add = os.getenv('hh')
    hh_add = os.environ.get('hh')
    # hh_add22 = os.environ.get('hh22')
    # hh_add33 = os.environ.get('hh33')
    # hh1 = hh.copy()

    time.sleep(1)
    #
    # bot.send_message(227722043, hh_add22)
    # bot.send_message(227722043, hh_add33)

    for i in hh_add:

        bot.send_message(227722043, i)



    for cook in hh_add:
        driver.add_cookie(cook)

    driver.refresh()
    time.sleep(1)


    # cookies = pickle.load(open("session", "rb"))
    # for cookie in cookies:
    #     driver.add_cookie(cookie)
    # driver.refresh()

    ob = driver.find_elements_by_class_name("HH-Supernova-NaviLevel2-Link")
    ob[0].click()

    ob1 = driver.find_elements_by_class_name('bloko-link_dimmed')

    bot.send_message(227722043, "here")

    for i in ob1:
        if i.text == 'Поднять в поиске':
            try:
                i.click()
                bot.send_message(-1001364950026, 'Подняли! :)')
            except:
                bot.send_message(-1001364950026, 'Что то не подняли :(')

    bot.send_message(-1001364950026, driver.current_url)

    bot.send_message(227722043, "Function Wake_up finished")



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


