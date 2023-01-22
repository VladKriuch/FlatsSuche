from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler


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
    "Kiel": "Kiel",
    "Rostock": "Rostock"
    }


class BasicHandler:
    def __init__(self, updater, dp, database_manager, helper):
        self.updater = updater
        self.dp = dp
        self.databaseManager = database_manager
        self.helper = helper
        self.handler = None

    def config_handler(self):
        pass

    def return_handler(self):
        return self.handler


class StartHandler(BasicHandler):
    def __init__(self, *args):
        BasicHandler.__init__(self, *args)
        self.config_handler()

    def config_handler(self):
        self.handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.handle_start)],
            states={
                "choosing_language": [
                    MessageHandler(Filters.all, self.choosing_language_on_start)
                ],
                "choosing_set_up_or_change_language": [
                    MessageHandler(Filters.text, self.choosing_set_up_or_change_language)
                ],
                "choosing_what_to_set_up": [
                    MessageHandler(Filters.text, self.choosing_what_to_set_up)
                ],
                "selecting_city":[
                    MessageHandler(Filters.text, self.selecting_city)
                ],
                "selecting_min_price":[
                    MessageHandler(Filters.text, self.selecting_min_price)
                ],
                "selecting_max_price": [
                    MessageHandler(Filters.text, self.selecting_max_price)
                ],
                "selecting_swap": [
                    MessageHandler(Filters.text, self.selecting_swap)
                ],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

    def handle_start(self, update, context):
        print("LOG:::")
        print("StartTriggered")
        print(update)

        if not update.message.from_user.is_bot:
            if not self.databaseManager.is_in_db({'chat_id': update.message.chat.id}):
                self.databaseManager.add_one({
                    'chat_id': update.message.chat.id,
                    'max_price': 1000000,                   # handle that shit
                    'min_price': 0,
                    'swap': 0,
                    'city': '',
                    'send_notification': False,
                    'language': 'EN'
                })
            self.databaseManager.edit_one({'chat_id': update.message.chat.id}, {'send_notification': False})


        bot = context.bot
        lang = self.databaseManager.get_first({'chat_id': update.message.chat.id})['language']
        bot.sendMessage(update.message.chat.id, self.helper.getPhrase("language_selection", lang),
                        reply_markup=self.helper.getKeyboard("SELECT_YOUR_LANGUAGE_KEYBOARD"))

        return "choosing_language"

    def choosing_language_on_start(self, update, context):
        text = update.message.text

        variants = {
            "🇬🇧󠁧󠁢󠁥󠁮󠁧󠁧": "EN",
            "🇩🇪": "DE"
        }

        bot = context.bot

        if text in variants or text in variants.values() or text == "🇬🇧󠁧":
            if text in variants:
                self.databaseManager.edit_one({'chat_id': update.message.chat.id}, {'language': variants[text]})
            elif text == "🇬🇧󠁧":
                self.databaseManager.edit_one({'chat_id': update.message.chat.id}, {'language': "EN"})
            else:
                self.databaseManager.edit_one({'chat_id': update.message.chat.id}, {'language': text})

            lang = self.databaseManager.get_first({'chat_id': update.message.chat.id})['language']
            bot.sendMessage(update.message.chat.id, self.helper.getPhrase("SET_UP_OR_CHANGE_LANGUAGE", lang),
                            reply_markup=self.helper.getKeyboard("twoOptionsKeyboard"))

            return "choosing_set_up_or_change_language"
        else:
            lang = self.databaseManager.get_first({'chat_id': update.message.chat.id})['language']
            bot.sendMessage(update.message.chat.id, self.helper.getPhrase("TRY_TO_SET_LANGUAGE_AGAIN", lang))
            return "choosing_language"

    def choosing_set_up_or_change_language(self, update, context):
        # ADD SOME FALLBACK MESSAGE
        text = update.message.text
        bot = context.bot

        lang = self.databaseManager.get_first({'chat_id': update.message.chat.id})['language']
        if text == "1":
            bot.sendMessage(update.message.chat.id, self.helper.getPhrase("CAN_CONFIGURATE_SETTINGS", lang))
            return self.settings_up(update, context)
        elif text == "2":
            return self.handle_start(update, context)
        else:
            bot.sendMessage(update.message.chat.id, self.helper.getPhrase("SET_UP_OR_CHANGE_LANGUAGE", lang),
                            reply_markup=self.helper.getKeyboard("twoOptionsKeyboard"))
            return "choosing_set_up_or_change_language"

    def settings_up(self, update, context):
        bot = context.bot
        lang = self.databaseManager.get_first({'chat_id': update.message.chat.id})['language']
        bot.sendMessage(update.message.chat.id, self.helper.getPhrase("CONFIGURATE_SETTINGS_MESSAGE", lang),
                        reply_markup=self.helper.getKeyboard("fiveOptionsKeyboard"))

        return "choosing_what_to_set_up"

    def choosing_what_to_set_up(self, update, context):
        text = update.message.text

        statesDict = {
            "1": "selecting_city",
            "2": "selecting_min_price",
            "3": "selecting_max_price",
            "4": "selecting_swap",
            "5": "start_searching"
        }
        lang = self.databaseManager.get_first({'chat_id': update.message.chat.id})['language']

        if text in statesDict:
            if text == "5":
                return self.start_searching(update, context)
            else:
                bot = context.bot
                keyboard = self.helper.getKeyboard(statesDict[text])
                if keyboard is None:
                    bot.sendMessage(update.message.chat.id, self.helper.getPhrase(statesDict[text], lang))
                else:
                    bot.sendMessage(update.message.chat.id, self.helper.getPhrase(statesDict[text], lang),
                                    reply_markup=self.helper.getKeyboard(statesDict[text]))

                return statesDict[text]
        else:
            #ADD SOME FALLBACK
            pass

    def start_searching(self, update, context):
        bot = context.bot

        lang = self.databaseManager.get_first({'chat_id': update.message.chat.id})['language']
        bot.sendMessage(update.message.chat.id, self.helper.getPhrase("GENERAL_MESSAGE", lang),
                        reply_markup=self.helper.getKeyboard("generalKeyboard"))

        self.databaseManager.edit_one({"chat_id": update.message.chat.id}, {"send_notification": True})
        return ConversationHandler.END

    def selecting_city(self, update, context):
        text = update.message.text
        bot = context.bot

        if text in locations.keys():
            self.databaseManager.edit_one({"chat_id": update.message.chat.id}, {"city": locations[text]})
            lang = self.databaseManager.get_first({'chat_id': update.message.chat.id})['language']
            bot.sendMessage(update.message.chat.id, self.helper.getPhrase("CHANGED_YOUR_CITY", lang))

        return self.settings_up(update, context)

    def selecting_max_price(self, update, context):
        text = update.message.text
        lang = self.databaseManager.get_first({'chat_id': update.message.chat.id})['language']

        if text.isnumeric():
            bot = context.bot
            min_price = self.databaseManager.get_first({"chat_id": update.message.chat.id})["min_price"]
            if int(text) < min_price:
                bot.sendMessage(update.message.chat.id,
                                self.helper.getPhrase("MAX_PRICE_LOWER", lang).replace("{{min_price}}", str(min_price)))
                return "selecting_max_price"
            else:
                self.databaseManager.edit_one({"chat_id": update.message.chat.id}, {"max_price": int(text)})
                bot.sendMessage(update.message.chat.id, self.helper.getPhrase("maxPriceEntered", lang).replace("{text}", text))
        else:
            # ADD SOME FALLBACK HERE
            pass

        return self.settings_up(update, context)

    def selecting_min_price(self, update, context):
        text = update.message.text
        lang = self.databaseManager.get_first({'chat_id': update.message.chat.id})['language']

        if text.isnumeric():
            bot = context.bot
            max_price = self.databaseManager.get_first({"chat_id": update.message.chat.id})["max_price"]
            if int(text) > max_price:
                bot.sendMessage(update.message.chat.id,
                                self.helper.getPhrase("MIN_PRICE_HIGHER", lang).replace("{{max_price}}", str(max_price)))
                return "selecting_min_price"
            else:
                self.databaseManager.edit_one({"chat_id": update.message.chat.id}, {"min_price": int(text)})
                bot.sendMessage(update.message.chat.id, self.helper.getPhrase("minPriceEntered", lang).replace("{text}", text))
        else:
            # ADD SOME FALLBACK HERE
            pass

        return self.settings_up(update, context)

    def selecting_swap(self, update, context):
        text = update.message.text
        bot = context.bot
        values = {
            "1": 1,
            "2": 0,
            "3": 2
        }
        if text.isnumeric() and int(text) in [1, 2, 3]:
            self.databaseManager.edit_one({"chat_id": update.message.chat.id}, {"swap": values[text]})
            phraseValues = {
                "1": "only swap",
                "2": "only no swap",
                "3": "both swap and no swap"
            }
            lang = self.databaseManager.get_first({'chat_id': update.message.chat.id})['language']
            bot.sendMessage(update.message.chat.id, self.helper.getPhrase("swapChanged", lang).replace(
                "{swaptext}", phraseValues[text]
            ))
        else:
            # ADD SOME FALLBACK HERE
            pass
        return self.settings_up(update, context)

    def cancel(self, update, context):
        update.message.reply_text('We`re sorry to say, but something gone wrong with bot, if you can'
                                  'please send us your feedback via somemail@gmail.com')

        # end of conversation
        return ConversationHandler.END


class SettingsHandler(StartHandler):
    def __init__(self, *args):
        BasicHandler.__init__(self, *args)
        self.config_handler()

    def config_handler(self):
        self.handler = ConversationHandler(
            entry_points=[MessageHandler(Filters.text('💤'), self.handle_settings)],
            states={
                "choosing_what_to_set_up": [
                    MessageHandler(Filters.text, self.choosing_what_to_set_up)
                ],
                "selecting_city":[
                    MessageHandler(Filters.text, self.selecting_city)
                ],
                "selecting_min_price":[
                    MessageHandler(Filters.text, self.selecting_min_price)
                ],
                "selecting_max_price": [
                    MessageHandler(Filters.text, self.selecting_max_price)
                ],
                "selecting_swap": [
                    MessageHandler(Filters.text, self.selecting_swap)
                ],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

    def handle_settings(self, update, context):
        self.databaseManager.edit_one({'chat_id': update.message.chat.id}, {'send_notification': False})
        return self.settings_up(update, context)


class DonateHandler(StartHandler):
    def __init__(self, *args):
        BasicHandler.__init__(self, *args)
        self.config_handler()

    def config_handler(self):
        self.handler = ConversationHandler(
            entry_points=[MessageHandler(Filters.text('💰'), self.donation_handle)],
            states={
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

    def donation_handle(self, update, context):
        bot = context.bot
        bot.sendMessage(update.message.chat.id, "This feature is in development")

        return ConversationHandler.END

class ChangeLanguageHandler(StartHandler):
    def __init__(self, *args):
        BasicHandler.__init__(self, *args)
        self.config_handler()

    def config_handler(self):
        self.handler = ConversationHandler(
            entry_points=[MessageHandler(Filters.text('🌐'), self.change_language_handle)],
            states={
                "choosing_language": [
                    CommandHandler('cancel', self.cancel),
                    MessageHandler(Filters.all, self.choosing_language)
                ],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

    def change_language_handle(self, update, context):
        self.databaseManager.edit_one({'chat_id': update.message.chat.id}, {'send_notification': False})

        bot = context.bot
        lang = self.databaseManager.get_first({'chat_id': update.message.chat.id})['language']
        bot.sendMessage(update.message.chat.id, self.helper.getPhrase("language_selection", lang),
                        reply_markup=self.helper.getKeyboard("SELECT_YOUR_LANGUAGE_KEYBOARD"))

        return "choosing_language"

    def choosing_language(self, update, context):
        text = update.message.text

        variants = {
            "🇩🇪": "DE",
            "🇬🇧󠁧󠁢󠁥󠁮󠁧󠁧": "EN"
        }
        bot = context.bot

        if text in variants or text in variants.values() or text == "🇬🇧󠁧":
            if text in variants:
                self.databaseManager.edit_one({'chat_id': update.message.chat.id}, {'language': variants[text]})
            elif text == "🇬🇧󠁧":
                self.databaseManager.edit_one({'chat_id': update.message.chat.id}, {'language': "EN"})
            else:
                self.databaseManager.edit_one({'chat_id': update.message.chat.id}, {'language': text})

            return self.start_searching(update, context)
        else:
            lang = self.databaseManager.get_first({'chat_id': update.message.chat.id})['language']
            bot.sendMessage(update.message.chat.id, self.helper.getPhrase("TRY_TO_SET_LANGUAGE_AGAIN", lang))
            return "choosing_language"
