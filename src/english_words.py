#!/usr/local/bin/python3

import os
import sys
from selenium import webdriver
from gyazo import Api
import json
import subprocess
import lookup_word


def main(args=sys.argv):
    # check arguments
    if len(args) == 1:
        print("Enter the first argument.")
        sys.exit()

    # look up English meaning
    search_word = args[1]
    meanings = lookup_word.main(search_word)

    # Google image search & save screenshot
    image_filename = 'screenshot.png'
    url = 'https://www.google.com/search?q={}&tbm=isch'.format(search_word)
    driver = webdriver.Chrome()
    driver.get(url)
    w = driver.execute_script('return document.body.scrollWidth')
    h = driver.execute_script('return document.body.scrollHeight')
    driver.set_window_size(w, h)
    driver.save_screenshot(image_filename)
    image_url = __upload_image(image_filename)

    # make scrapbox page
    PROJECT_URL = 'https://scrapbox.io/eda-englishwords/'
    __make_scrapbox_page(PROJECT_URL, search_word, image_url, meanings)


def __upload_image(image_filename):
    if "API_TOKEN" not in os.environ:
        print("command `export API_TOKEN=hoge`")

    API_TOKEN = os.environ.get("API_TOKEN")
    client = Api(access_token=API_TOKEN)

    # Upload an image
    with open(image_filename, 'rb') as f:
        image = client.upload_image(f)
        image_json = image.to_json()
        image_dict = json.loads(image_json)
        image_url = image_dict['url']

    return image_url


def __make_scrapbox_page(project_url, english_word, image_url, meanings):
    image_tag = '[' + image_url + ']'

    linefeed_code = '%0A'
    scrapbox_url = project_url + english_word
    scrapbox_url += '?body='
    for meaning in meanings:
        scrapbox_url += ' [[' + meaning + ']]' + linefeed_code
    scrapbox_url += image_tag

    print(scrapbox_url)
    subprocess.run(["open", scrapbox_url])


if __name__ == "__main__":
    main()
