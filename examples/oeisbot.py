from mastobot import *
from oeis.client import entry
from os import environ
from datetime import datetime
import re

bot = Bot(environ.get("INSTANCE"), environ.get("ACCESS_TOKEN"), websocket_mode=True)


@bot.on_mention("A[0-9]{6}", validation=REGEX)
def get_sequence(status):
    serial = re.search("(A[0-9]{6})", status.text).group()
    sequence = entry(serial)
    if sequence:
        created = datetime.fromisoformat(sequence.created)
        return (
            f"OEIS {serial}: {sequence.name}\n\n"
            + sequence.data
            + f"\n\nCreated at {created.year}-{created.month}-{created.day}\n\n"
            f"https://oeis.org/{serial}"
        )
    else:
        return f"OEIS {serial} not found."


bot.run()
