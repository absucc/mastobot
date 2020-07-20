from mastobot import *
from os import environ

if __name__ == "__main__":
    instance = environ.get("INSTANCE")
    token = environ.get("ACCESS_TOKEN")
    bot = Bot(instance, token)

    @bot.on_mention("henlo", validation=EQUALS)
    def respond(status):
        return "hi, " + status.account.display_name

    @bot.on_home_update("mastobot", validation=CONTAINS)
    def online(status):
        return "yes i am online why do you ask"

    bot.run()
