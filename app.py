import os
from selenium import webdriver
import telebot
from flask import Flask, request
from config import *
import pickle

bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-sh-usage')

driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)


# driver.get('https://hh.ru/')
# print(driver.page_source)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Bot works")


@bot.message_handler(commands=['res'])
def send_welcome(message):

    bot.send_message(message.from_user.id, "RES command starts")

    driver.get('https://hh.ru/')
    print(driver.current_url)

    cookies = pickle.load(open("session", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()

    driver.find_element_by_class_name("HH-Supernova-NaviLevel2-Link")

    ob = driver.find_elements_by_class_name('applicant-resumes-update-button')

    bot.send_message(message.from_user.id, driver.current_url)

    for item in ob:
        bot.send_message(message.from_user.id, 'Its a cycle')
        bot.send_message(message.from_user.id, item.text)

    bot.send_message(message.from_user.id, "2 RES command finished")



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


