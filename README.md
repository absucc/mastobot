# Mastobot - cheap mastodon bots

## Examples

### Basic usage

```python
from mastobot import Bot
bot = Bot(
    instance_url="https://mastodon.instance",
    access_token="your_access_token",
)

@bot.on_mention("hi")
def respond_to_hi(notification):
    name = notification["status"]["account"]["username"]
    return f"hey, {name}!"

bot.run()
```

### Advanced usage

**WIP**

## Installation

It's not on PyPI yet. Mastobot is such a good name, it took me eight seconds to come up with it. I anticipate that it will be, soon.

### Install via setuptools

Clone and cd into this repo, `python setup.py install --user`.
