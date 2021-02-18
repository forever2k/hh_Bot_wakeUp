import telebot
from flask import Flask, request
from config import *
import requests
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import time

bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)

URL = 'https://hh.ru/'

class HHParser:

    def __init__(self, driver):
        self.driver = driver
        driver.implicitly_wait(4)

    def resume_wake_up(self):
        driver.get(URL)
        # pickle.dump(driver.get_cookies(), open("session", "wb"))
        # time.sleep(100)
        # print('save')
        cookies = pickle.load(open("session", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()

        driver.find_element_by_class_name("HH-Supernova-NaviLevel2-Link").click()

        resumeUp = driver.find_elements_by_class_name("applicant-resumes-update-button")
        for resume in resumeUp:
            try:
                resume.click()
            except:
                pass


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Bot works")

def resume_schedule():
    main()
    parser = HHParser(driver)
    parser.resume_wake_up()
    bot.send_message(-1001364950026, "Resumes were updated")


#
# def photo_schedule():
#     main()
#     parser = PictureParser(driver)
#     link = parser.get_link()
#     quit()
#     bot.send_photo(-1001364950026, photo=link)
#
#
def main():
    global driver
    chrome_options = Options()
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                'like Gecko) Chrome/85.0.4183.83 Safari/537.36')
    # chrome_options.add_argument('headless')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=chrome_options)


schedule.every(3).minutes.do(resume_schedule)

while True:
    schedule.run_pending()


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
