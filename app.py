import os
from selenium import webdriver
import telebot
from flask import Flask, request
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

URL = 'https://hh.ru/'




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

    schedule.every(60).minutes.do(girl)

    while True:
        schedule.run_pending()
        time.sleep(1)

    # bot.send_message(message.from_user.id, "Its END of Send")


def girl():
    page = random.randrange(1, 10)
    URL2 = 'https://xxx.pics/category/cute/' + str(page) + '/'
    guys = ['парни', 'ребятушки', 'братушки', 'ребятки', 'мужики', 'перцы', 'эксперты', 'экспертное сообщество', 'мои герои', 'сладкие мои']
    greeting = ['здарова', 'хая', 'салам', 'салют', 'здравствуйте', 'шалом', 'бонжур', 'хэллоу', 'хей', 'буэнос диас',
                'хола', 'доброго дня', 'добрый день', 'ассалам алейкум']
    phrases = ['как вам мои чики?', 'попробуйте меня', 'какая я вкусненькая', 'смотрите на мои вишенки',
               'как вам мои изюминки?', 'я вся горю', 'початимся?', 'пообщаемся?',
               'ох, не смотри на меня так', 'мои булочки готовы для вас', 'рада тут побывать',
               'всегда готова, жду вас тут', 'порадуйте меня чем нибудь', 'я секси, да?', 'я конфетка, да?',
               'сейчас позову подружек не хуже меня', 'сегодня здесь будет жарко', 'я вся горю',
               'классный денек сегодня, да?', 'погодка не фонтан, согрейте меня', 'всем хорошего дня!',
               'всем классного дня!', 'заходите поглядеть на меня еще', 'хватит палитьтся на мои титьки', 'как я вам?', 'оцените меня экспертно', 'не сломайте об меня глаза']
    emoji = ['$)', ':)', ';)', 'oO', ':**', ' ', '..', 'уух', 'мм;)']

    guys_random = random.randrange(0, len(guys))
    greeting_random = random.randrange(0, len(greeting))
    phrases_random = random.randrange(0, len(phrases))
    emoji_random = random.randrange(0, len(emoji))

    willing_phrase = f'{guys[guys_random].capitalize()} {greeting[greeting_random]}! {phrases[phrases_random].capitalize()} {emoji[emoji_random]}'

    driver.get(URL2)
    bot.send_message(227722043, 'here 0')

    try:
        path_to_pict = driver.find_elements_by_class_name('pcsrt-th-lightgallery-item')

        bot.send_message(227722043, 'here 1')

        all_pict = len(path_to_pict)
        pict_random = random.randrange(0, all_pict)

        bot.send_message(227722043, 'here 2')

        pict = path_to_pict[pict_random].get_attribute('data-src')

        bot.send_message(227722043, 'here 3')

        bot.send_photo(227722043, photo=pict)
        bot.send_message(227722043, willing_phrase)

    except Exception as error:
        bot.send_message(227722043, error)


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


