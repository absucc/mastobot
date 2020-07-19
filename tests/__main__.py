from mastobot import *

if __name__ == "__main__":
    bot = Bot("https://yeet.social", "pMkDvctDbWEv5nL8zfTtm_X0LPmosbnj-h9I59s7Z8o")

    @bot.on_mention("@c18n henlo", validation=EQUALS)
    def respond(notif):
        return "hi, " + notif["status"]["account"]["username"]

    @bot.on_home_update("mastobot", validation=CONTAINS)
    def online(status):
        return "yes i am online why do you ask"

    bot.run()
