import os
from selenium import webdriver
import telebot
from flask import Flask, request
from config import *
import pickle
import schedule
import time
import random

bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-sh-usage')

driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)


URL = 'https://hh.ru/'

page = random.randrange(1, 10)
URL2 = 'https://xxx.pics/category/cute/' + str(page) + '/'


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Bot works")
    bot.send_message(message.from_user.id, message.from_user.id)


@bot.message_handler(commands=['res'])
def send_welcome(message):

    bot.send_message(message.from_user.id, "RES command starts")

    schedule.every(250).minutes.do(wake_up)

    while True:
        schedule.run_pending()
        time.sleep(1)

    bot.send_message(message.from_user.id, "Its END of RES")


@bot.message_handler(commands=['send'])
def send_girl(message):
    bot.send_message(message.from_user.id, "Send Bot works")
    driver.get(URL2)

    ob = driver.find_elements_by_class_name("pcsrt-th-pics")
    ob[1].click()
    r = driver.current_url
    url = r.url

    bot.send_photo(message.from_user.id, photo=url)
    bot.send_photo(message.from_user.id, photo=r)
    bot.send_photo(message.from_user.id, photo=ob[1])
    bot.send_photo(message.from_user.id, driver.current_url)



def wake_up():

    bot.send_message(227722043, "Function Wake_up starts")
    driver.get(URL)

    cookies = pickle.load(open("session", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()

    ob = driver.find_elements_by_class_name("HH-Supernova-NaviLevel2-Link")
    ob[0].click()

    ob1 = driver.find_elements_by_class_name('bloko-link_dimmed')

    for i in ob1:
        if i.text == 'Поднять в поиске':
            try:
                i.click()
                bot.send_message(-1001364950026, 'Подняли! :)')
            except:
                bot.send_message(-1001364950026, 'Что то не подняли :(')

    bot.send_message(-1001364950026, driver.current_url)

    bot.send_message(227722043, "Function Wake_up finished")


# schedule.every(3).minutes.do(wake_up)

# while True:
#     schedule.run_pending()
#     time.sleep(1)


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


