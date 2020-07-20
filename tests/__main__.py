from mastobot import *
from os import environ

if __name__ == "__main__":
    instance = environ.get("INSTANCE")
    token = environ.get("ACCESS_TOKEN")
    bot = Bot(instance, token)

    @bot.on_mention("henlo", validation=EQUALS)
    def respond(status):
        return "hi, " + status.account.display_name

    has_more_than_two_cates = lambda s: s.count(":cate:") > 2

    @bot.on_home_update(has_more_than_two_cates, validation=EVALUATE)
    def so_many_cates(status):
        cate_count = status.content.count(":cate:")
        return Reply(
            f"Woah, {cate_count} cates - that's a lot!",
            visibility=UNLISTED,
            sensitive=False,
        )

    @bot.on_home_update("mastobot", validation=CONTAINS)
    def online(status):
        return "yes i am online why do you ask"

    bot.run()
