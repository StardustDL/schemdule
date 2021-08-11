import json
import logging
import time
from typing import Any
from urllib import parse, request

from schemdule.prompters import (Prompter, PrompterPayloadCollection,
                                 PromptResult, getMessage)

__version__ = "0.0.8"


class MiaotixingPrompter(Prompter):
    _logger = logging.getLogger("MiaotixingPrompter")

    def __init__(self, code: str, final: bool = False) -> None:
        super().__init__(final)
        self.code = code

    def prompt(self, payloads: PrompterPayloadCollection) -> PromptResult:
        with request.urlopen("http://miaotixing.com/trigger?" + parse.urlencode({"id": self.code, "text": getMessage(payloads), "type": "json"})) as req:
            result = json.loads(req.read())
        if result["code"] == 0:
            return self.success()
        else:
            self._logger.error(
                f"Failed with code {result['code']}: {result['msg']}.")
            if self.final:
                return PromptResult.Failed
