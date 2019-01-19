#!/usr/local/bin/python3
import sys
from urllib.request import urlopen
import json
import click
from meaning import Meaning

BASE_URL = "https://glosbe.com/gapi/translate"


def get_url(phrase):
    """Glosbe API により、引数に与えられた単語の翻訳を取得

    :param phrase:
    """
    tarnslated_ja = "?from=en&dest=ja"
    phrase_arg = f"&phrase={phrase}"
    url = f"{BASE_URL}{tarnslated_ja}&format=json{phrase_arg}&pretty=true"
    return url


def load_json(json_data):
    loaded = json.loads(json_data)['tuc']
    if not loaded:
        raise click.exceptions.BadParameter("検索した結果,見つかりませんでした")

    for json_dict in loaded:
        yield json_dict


def main(phrase=sys.argv[1]):

    num = 3
    url = get_url(phrase)
    response = urlopen(url)
    json_data = response.read().decode("utf-8")
    data = load_json(json_data)

    for counter, mean_pair in enumerate(data):

        if counter == 0:
            print(f'=== {phrase}の意味 ==================')
        if counter > num - 1:
            break

        try:
            japanese = mean_pair['phrase']['text']
        except KeyError:
            raise click.BadParameter("見つかりませんでした")
        english = mean_pair['meanings'] if 'meanings' in mean_pair else None
        mean = Meaning(phrase, japanese, english)
        mean.look_up()
        print("=================================")


if __name__ == '__main__':
    main()
