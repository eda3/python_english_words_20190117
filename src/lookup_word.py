#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys
from urllib.request import urlopen
import json
from meaning import Meaning
import pprint

BASE_URL = "https://glosbe.com/gapi/translate"


def get_url(phrase):
    """Glosbe API により、引数に与えられた単語の翻訳を取得

    :param phrase:
    """
    tarnslated_ja = "?from=en&dest=ja"
    phrase_arg = f"&phrase={phrase}"
    url = f"{BASE_URL}{tarnslated_ja}&format=json{phrase_arg}&pretty=true"
    return url


def __get_english_meanings(datas, limit):
    num = 0
    meanings = []
    for data in datas:
        if 'meanings' in data:
            for meaning in data['meanings']:
                meanings.append(meaning['text'])
                num += 1
                if num >= limit:
                    return meanings


def main(phrase=sys.argv[1]):
    url = get_url(phrase)
    response = urlopen(url)
    json_data = response.read().decode("utf-8")
    loaded = json.loads(json_data)['tuc']
    return __get_english_meanings(loaded, 3)


if __name__ == '__main__':
    main()
