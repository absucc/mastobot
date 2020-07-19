from .constants import VISIBILITY_LIST


class Reply:
    """Helper class exposed to the bot developer. Avoids quirky dict syntax
        because ``reply.key`` is so much more succint than ``dict["key"]``.
    """

    def __init__(self, text: str, sensitive=None, visibility=None, spoiler_text=None):
        self.text = str(text)
        if not type(sensitive) == bool:
            raise ValueError("Argument `sensitive` must be a boolean")
        self.sensitive = sensitive
        if not visibility in VISIBILITY_LIST:
            raise ValueError(
                "Argument `visibility` must be one of "
                "'public', 'unlisted', 'private', or 'direct'"
            )
        self.visibility = visibility
        self.spoiler_text = spoiler_text
