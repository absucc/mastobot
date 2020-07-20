# Mastobot - cheap mastodon bots

## Important

Nothing in this project is set in stone except that it's for cheap bots only. Consider your use cases before adopting this library. Mastobot is suitable for bots which do not require intensive interaction, e.g. media or polls. Just write your own bot from scratch if you want juicy features. It also aims to be beginner-friendly, even (especially) those who don't understand decorators. You're welcome to contribute if you do.

## Examples

### Basic usage

```python
from mastobot import Bot
bot = Bot(
    instance_url="https://mastodon.instance",
    access_token="your_access_token",
)

@bot.on_mention("hi")
def respond_to_hi(status):
    name = status.account.username
    return f"hey, {name}!"

bot.run()
```

### Advanced usage

**WIP**

## Installation

It's not on PyPI yet. Mastobot is such a good name, it took me eight seconds to come up with it. I anticipate that it will be, soon.

### Install via setuptools

Clone and cd into this repo, `python setup.py install --user`.
