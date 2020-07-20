from .constants import *


class Trigger:
    def __init__(self, event: str, validation: str, expectation, callback):
        """Describes a condition that would trigger a callback.

        :param event: (str) may be "mention", "favourite", "reblog", "follow", or "update".
        :param validation: (str) may be "equals", "contains", "regex" or "evaluate".
        :param expectation: (str or callable) string, regex string or function
            to test content of relevant status against.

            Suppose the normalized (html-to-text converted) content of the status
            received is ``content``.

            If ``validation`` is "equals", the trigger will be invoked when
            content exactly matches expectation; if it is ``contains``, when
            expectation is found anywhere in content; if it is ``regex``,
            when content regex-matches expectation; if it is ``evaluate``,
            when ``expectation(content) == True``.            
            
        :param callback: (callable) callback executed when self is triggered.
            Arguments passed to it depend on ``event``.
        """
        if event not in EVENT_LIST:
            raise ValueError("Trigger event incorrect")
        elif validation not in VALIDATION_LIST:
            raise ValueError("Trigger validation incorrect")
        elif not callable(callback):
            raise ValueError("Trigger callback not callable")

        self.event = event
        self.validation = validation
        self.expectation = expectation
        self.callback = callback

    def test(self, event: str, content: str):
        """Test if self should be triggered.

        :param event: (str) event that invoked this test.
        :param content: (str) normalized status content.
        """

        if not event == self.event:
            return

        if self.validation == EQUALS:
            return content == self.expectation
        elif self.validation == CONTAINS:
            return content.find(self.expectation) > -1
        elif self.validation == REGEX:
            raise NotImplementedError
        elif self.validation == EVALUATE:
            raise NotImplementedError

    def invoke(self, obj):
        return self.callback(obj)
