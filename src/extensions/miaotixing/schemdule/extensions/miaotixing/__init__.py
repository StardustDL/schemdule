from typing import Any
from schemdule.prompters import Prompter, PromptResult
from urllib import request, parse
import time
import json
import logging

__version__ = "0.0.7"


class MiaotixingPrompter(Prompter):
    _logger = logging.getLogger("MiaotixingPrompter")

    def __init__(self, code: str, final: bool = False) -> None:
        super().__init__(final)
        self.code = code

    def prompt(self, message: str, payload: Any) -> Any:
        with request.urlopen("http://miaotixing.com/trigger?" + parse.urlencode({"id": self.code, "text": message, "type": "json"})) as req:
            result = json.loads(req.read())
        if result["code"] == 0:
            return self.success()
        else:
            self._logger.error(
                f"Failed with code {result['code']}: {result['msg']}.")
            if self.final:
                return PromptResult.Failed