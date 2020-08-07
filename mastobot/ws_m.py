import websockets
import asyncio
import urllib
import json
from .constants import *


class WebsocketsListener:
    def __init__(self, instance: dict, access_token: str, stream="user"):
        """Initiate a WebSockets Listener

        :param instance: (dict) Mastodon.py dict of the instance
        :param access_token: (str)
        :param stream: (str)
        """

        self._instance = instance["uri"]
        try:
            self._ws_endpoint = urllib.parse.urljoin(
                instance["urls"]["streaming_api"],
                f"/api/v1/streaming?access_token={access_token}&stream={stream}",
            )
        except KeyError:
            raise Exception(
                f"The instance {instance['uri']} did not provide a WebSockets URL"
            )

    async def _stream(self):
        async with websockets.connect(self._ws_endpoint) as socket:
            while True:
                received = await socket.recv()
                print(received)

    def start_stream(self):
        asyncio.get_event_loop().run_until_complete(self._stream())

wsl = WebsocketsListener({"uri":"mastodon.technology", "urls": {"streaming_api": "wss://mastodon.technology"}}, "WDBFPHZpZcMFCl2ShLxOgzIJWoqEAmDKs1rGKVNS3rA")
wsl.start_stream()
