import json
import logging
import time
from typing import Any
from urllib import parse, request

from schemdule.helpers import buildMessage
from schemdule.prompters import PayloadCollection, Prompter, PromptResult

__version__ = "0.0.9"


class MiaotixingPrompter(Prompter):
    _logger = logging.getLogger("MiaotixingPrompter")

    def __init__(self, code: str, final: bool = False) -> None:
        super().__init__(final)
        self.code = code

    def prompt(self, payloads: PayloadCollection) -> PromptResult:
        with request.urlopen("http://miaotixing.com/trigger?" + parse.urlencode({"id": self.code, "text": buildMessage(payloads), "type": "json"})) as req:
            result = json.loads(req.read())
        if result["code"] == 0:
            return self.success()
        else:
            self._logger.error(
                f"Failed with code {result['code']}: {result['msg']}.")
            if self.final:
                return PromptResult.Failed
