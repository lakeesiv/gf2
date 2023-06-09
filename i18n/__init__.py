
import json
import os
from typing import List, Optional

locales = ["en_GB", "ru_RU", "en_US", "fr_FR", "el_GR", "es_ES"]


class Translate:
    def __init__(self, module, locale=None):
        self.locale = os.environ.get("LANG", "en_GB").split(".")[0]
        if locale is not None:
            self.locale = locale
        if self.locale not in locales:
            self.locale = "en_GB"
        self.module = module

    def __call__(self, id, values: Optional[List[str]] = None):
        # open file
        with open("i18n/" + self.locale + ".json", "r", encoding="utf8") as f:
            # read file
            data = json.load(f)
            try:
                id = self.module + "." + id
                text = data[self.module][id]

                # replace placeholders with values
                if values is not None:
                    for i in range(len(values)):
                        text = text.replace("{" + str(i) + "}", values[i])
                return text

            except BaseException:
                return "Error: Failed to load translation"
