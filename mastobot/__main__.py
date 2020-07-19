from mastodon import Mastodon, StreamListener
from .html_text import html_to_text
from .reply import Reply
from .trigger import Trigger
from .constants import *

# related documentation: https://mastodonpy.readthedocs.io/en/stable/#


class Bot:
    def __init__(self, instance_url: str, access_token: str):
        """Intiate a Mastodon bot.

        :param instance_url: (str) base URL for your Mastodon instance of choice,
            e.g. ``https://mastodon.technology``.
        :param access_token: (str) "Your access token" inside
            Preferences -> Development -> some application.
        """
        self._instance = instance_url
        self._token = access_token
        self._triggers = []
        self._check_update_triggers = lambda o: self._check_triggers(o, UPDATE)
        self._check_notification_triggers = lambda o: self._check_triggers(
            o, NOTIFICATION
        )

    def _check_triggers(self, obj: dict, stream: str):
        """Handle events from ``mastodon.StreamListeupdate_ner.on_update()`` if 
            ``stream=="update"``, and ``mastodon.StreamListener.on_notification()``
            if ``stream=="notification"``.
        """
        # TODO if the bot is mentioned, strip the mention text @bot

        for trig in self._triggers:
            if stream == trig.event == UPDATE and trig.test(
                UPDATE, html_to_text(obj["content"])
            ):
                self._reply(obj, trig.invoke(obj))
            elif (
                stream == NOTIFICATION
                and trig.event == obj["type"]
                and trig.test(obj["type"], html_to_text(obj["status"]["content"]))
            ):
                self._reply(obj["status"], trig.invoke(obj))

    def _reply(self, status: dict, content):
        """Reply to a status with content.

        :param status: (dict) the status to reply to.
        :param content: (str or mastobot.Reply) When ``content`` is a string,
            simply reply with it, keeping everything else as Mastodon.py decides.
            When it is an instance of the ``mastobot.Status`` class, all its arguments
            will be passed on to Mastodon.py. The rest are left in their default state.
        """
        if not content:
            raise ValueError(f"Status content empty; reply to {status['id']} aborted")
        elif type(content) == str:
            args = {
                STATUS: content,
                SENSITIVE: status[SENSITIVE],
                VISIBILITY: status[VISIBILITY],
                SPOILER_TEXT: status[SPOILER_TEXT],
            }
        elif isinstance(content, Reply):
            args = {
                STATUS: content.text,
                VISIBILITY: content.visibility or status[VISIBILITY],
                # awkward syntax because content.sensitive can be False
                # in which case `content.sensitive or status["sensitive"]`
                SENSITIVE: (
                    content.sensitive
                    if content.sensitive is not None
                    else status[SENSITIVE]
                ),
                SPOILER_TEXT: content.spoiler_text or status[SPOILER_TEXT],
            }

        self._bot.status_reply(to_status=status, in_reply_to_id=status["id"], **args)

    # decorator generators

    def on_mention(self, expectation, validation=EQUALS):
        """Listen to mentions and invoke a callback with the Mastodon.py
            notification dict as argument.

        :param expectation: (str or callable) string, regex string or callable
            that evaluates to True if the status content is what you want.
        :param validation: (str) may be "equals", "contains", "regex" or "evaluate".
        """

        def decorator(callback):
            self._triggers.append(
                Trigger(
                    event=MENTION,
                    validation=validation,
                    expectation=expectation,
                    callback=callback,
                )
            )

        return decorator

    def on_home_update(self, expectation, validation=EQUALS):
        """Listen to updates on the home timeline and invoke a callback with
            the Mastodon.py status (toot) dict as argument.

        :param expectation: (str or callable) string, regex string or callable
            that evaluates to True if the status content is what you want.
        :param validation: (str) may be "equals", "contains", "regex" or "evaluate".
        """

        def decorator(callback):
            self._triggers.append(
                Trigger(
                    event=UPDATE,
                    validation=validation,
                    expectation=expectation,
                    callback=callback,
                )
            )

        return decorator

    # execution

    def run(self):
        """Start bot.

        After all listeners (triggers) are set, invoke ``bot.run()``.
        """
        self._bot = Mastodon(api_base_url=self._instance, access_token=self._token)
        print("Connected to " + self._instance)

        # register stream listeners
        self._user_stream = StreamListener()
        self._user_stream.on_update = self._check_update_triggers
        self._user_stream.on_notification = self._check_notification_triggers
        self._bot.stream_user(self._user_stream)
