import os
from selenium import webdriver
import telebot
from flask import Flask, request
from config import *
import pickle
import schedule
import time

bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-sh-usage')

driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)


URL = 'https://hh.ru/'


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Bot works")
    bot.send_message(message.from_user.id, message.from_user.id)


@bot.message_handler(commands=['res'])
def send_welcome(message):

    bot.send_message(message.from_user.id, "RES command starts")

    schedule.every(1).minutes.do(wake_up)

    while True:
        schedule.run_pending()
        time.sleep(1)

def wake_up():
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

    bot.send_message(-1001364950026, "Updated finished")


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


