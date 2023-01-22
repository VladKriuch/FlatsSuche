from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
locations = \
    {
    "Berlin": "Berlin",
    "Hamburg": "Hamburg",
    "München": "Muenchen",
    "Frankfurt am Main": "Frankfurt_main",
    "Hannover": "Hannover",
    "Leipzig": "Leipzig",
    "Dresden": "Dresden",
    "Dortmund": "Dortmund",
    "Köln": "Koeln",
    "Düsseldorf": "Duesseldorf",
    "Bremen": "Bremen",
    "Stuttgart": "Stuttgart",
    "Nürnberg": "Nuernberg",
    "Essen": "Essen",
    "Bonn": "Bonn",
    }

class HELPERS:
    def __init__(self, phrases):
        # self.setUpPhrases()
        self.createKeyboards()
        self.phrases = phrases

    def getPhrase(self, phraseName, language="EN"):
        return self.phrases[language][phraseName]

    def getKeyboard(self, keyboardName):
        try:
            return self.keyboardDict[keyboardName]
        except Exception:
            return None

    def createKeyboards(self):
        selectYourLanguageKeyboardBttns = [[KeyboardButton("🇩🇪"), KeyboardButton("🇬🇧󠁧")]]
        selectYourLanguageKeyboard = ReplyKeyboardMarkup(selectYourLanguageKeyboardBttns, resize_keyboard=True)

        twoOptionsKeyboard = ReplyKeyboardMarkup([[KeyboardButton("1"), KeyboardButton("2")]], resize_keyboard=True)

        fiveOptionsKeyboard = ReplyKeyboardMarkup([[KeyboardButton("1"), KeyboardButton("2"),
                                                    KeyboardButton("3"), KeyboardButton("4"),
                                                    KeyboardButton("5")]], resize_keyboard=True)

        generalKeyboard = ReplyKeyboardMarkup([[KeyboardButton("💤"), KeyboardButton("🌐"), KeyboardButton("💰")]],
                                              resize_keyboard=True)

        cityKeyboardBttns = []
        tempArr = []
        for location in locations:
            if len(tempArr) == 2:
                tempBttnsArr = [KeyboardButton(tempArr[0]), KeyboardButton(tempArr[1])]
                cityKeyboardBttns.append(tempBttnsArr)
                tempArr = []
            tempArr.append(location)

        if len(tempArr) == 1:
            tempBttnsArr = [KeyboardButton(tempArr[0])]
            cityKeyboardBttns.append(tempBttnsArr)

        cityKeyboard = ReplyKeyboardMarkup(cityKeyboardBttns, resize_keyboard=True)
        swap_keyboard_bttns = [KeyboardButton("1"), KeyboardButton("2"), KeyboardButton("3")]
        swap_keyboard = ReplyKeyboardMarkup([swap_keyboard_bttns], resize_keyboard=True)
        self.keyboardDict = {
            "SELECT_YOUR_LANGUAGE_KEYBOARD": selectYourLanguageKeyboard,
            "twoOptionsKeyboard": twoOptionsKeyboard,
            "fiveOptionsKeyboard": fiveOptionsKeyboard,
            "generalKeyboard": generalKeyboard,
            "selecting_city": cityKeyboard,
            "selecting_swap": swap_keyboard
        }
