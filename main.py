import bot
from dbmanager import PyMongoDBManager

from threading import Thread
from time import sleep
import parse
import requests
import json
from helpers import HELPERS

import logging
import socket
from logging.handlers import SysLogHandler


class ContextFilter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True


def notification_users(databaseManager, parser, url):
    """
        THREAD WHERE ALL NOTIFICATIONS FOR USERS WILL BE HAPPENED
    """
    print("Thread running...")
    TIME_IN_SECONDS = 10
    print(f"Thread time: {TIME_IN_SECONDS}")
    while True:
        sleep(TIME_IN_SECONDS)
        print(f"{TIME_IN_SECONDS} seconds passed... running parser")
        AllChats = databaseManager.get_many({'send_notification': True})
        allCities = []
        allSwaps = []
        for data in AllChats:
            allCities.append(data["city"])
            allSwaps.append(data["swap"])
        allCities = set(allCities)
        print(data for data in AllChats)
        allSwaps = set(allSwaps)
        print("All chats in db::::")
        print(AllChats)
        print(":::::::")
        print("All cities in db: ")
        print(allCities)
        print(f"All swaps in db: {allSwaps}")
        if len(allCities) == 0:
            continue
        for city in allCities:
            for swap in allSwaps:
                if databaseManager.is_in_db({'location': city, 'swap': swap}) is None:
                    continue
                parser.make(location=city, swap=swap)
                print("\n::::::ITEMS::::::")
                parsed_items = parser.get_list("ebay", city, swap)
                print("parsed_items")
                print(parsed_items)
                print(":::::::::::::::::\n")

                users = databaseManager.get_many({'city': city, 'swap': swap})
                for value in users:
                    for item in parsed_items:
                        try:
                            if value["min_price"] < int(item.price) < value["max_price"]:
                                # self.updater.bot.sendMessage(value.chat_id, f'Url: {item.url} \n Price = {item.price}')
                                message = f"{item.description}\n" \
                                          f"*{item.price} €*\n" \
                                          f"Address is *{item.address}*\n" \
                                          f"[⁠]({item.img})"
                                          # f"<a href=\"{item.url}\">URL</a>\n" \
                                url_for_request = url
                                url_for_request = url_for_request.replace("{chat_id}", str(value["chat_id"]))
                                url_for_request = url_for_request.replace("{parse_mode}", "markdown")
                                url_for_request = url_for_request.replace("{text}", message)
                                url_for_request = url_for_request.replace("{item_url}", item.url)
                                # url_for_request = url_for_request.replace("{inline_keyboard}", str(inline_markup))
                                print("url_for_request")
                                print(url_for_request)
                                requests.get(url_for_request)
                        except Exception:
                            pass
                    # url_for_request = url
                    # url_for_request = url_for_request.replace("{chat_id}", str(value["chat_id"]))
                    # url_for_request = url_for_request.replace("{parse_mode}", "HTML")
                    # requests.get(url_for_request)


def loggerInit():
    syslog = SysLogHandler(address=('logs6.papertrailapp.com', 52605))
    syslog.addFilter(ContextFilter())
    format = '%(asctime)s %(hostname)s LOG: %(message)s'
    formatter = logging.Formatter(format, datefmt='%b %d %H:%M:%S')
    syslog.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(syslog)
    logger.setLevel(logging.INFO)

    return logger


if __name__ == '__main__':
    """logger"""
    logger = loggerInit()

    logger.info("-")
    logger.info("-")
    logger.info("-")
    logger.info("-")
    logger.info("-")
    logger.info("-")
    logger.info("##################################")
    logger.info("#         Bot is started         #")
    logger.info("##################################")

    with open("config_bot.json") as file:
        data = json.load(file)
        botData = data['bot']

    with open("config_phrases.json", encoding='utf-8') as file:
        data = json.load(file)
        phrases = data['phrases']

    with open('config_parse.json') as file:
        parseData = json.load(file)

    token = botData['BotToken']

    url = "https://api.telegram.org/bot<token>/sendMessage?chat_id={chat_id}&parse_mode={parse_mode}&text={text}" \
          "&disable_web_page_preview=false&" \
          "reply_markup={\"inline_keyboard\": [[{\"text\": \"URL\", \"url\": \"{item_url}\"}]]}"
    url = url.replace("<token>", token)

    databaseManager = PyMongoDBManager(connection_string=botData['CONNECTION_STRING'],
                                       target_db_name=botData['TARGET_DB_NAME'],
                                       target_collection_name=botData['TARGET_COLLECTION_NAME'])

    """parser"""
    parser = parse.PARSER(parseData, logger)
    helpers = HELPERS(phrases)



    notificThread = Thread(target=notification_users, args=(databaseManager, parser, url, ))
    notificThread.start()
    botUpdater = bot.BOT(token, databaseManager, helpers)

    botUpdater.run()
