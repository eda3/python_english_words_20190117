#!/usr/bin/env python3
import re


class Meaning:
    def __init__(self, phrase, japanese, english=None):
        self.phrase = phrase
        self.japanese = japanese
        self.english = english

    def look_up(self):
        print("* " + self.japanese + ' *')
        if self.english:
            self._extract_mean()
        else:
            print("適切な英語の説明がありませんでした。")

    def _extract_mean(self):
        for i, mean in enumerate(self.english, 1):
            text = mean['text']
            eg_regex = re.search('e.g.', text)
            esp_regex = re.search('esp.', text)
            if not any([eg_regex, esp_regex]):
                text = text.replace('. ', '.\n\t')
            else:
                text = mean['text']

            if mean['language'] == 'ja':
                continue
            print(f"意味{i} : {text}")
