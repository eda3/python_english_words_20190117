#!/usr/local/bin/python3

import os
import sys
from selenium import webdriver
from gyazo import Api
import json
import subprocess


def main(args=sys.argv):
    # check arguments
    if len(args) == 1:
        print("Enter the first argument.")
        sys.exit()

    # Google image search & save screenshot
    image_filename = 'screenshot.png'
    url = 'https://www.google.com/search?q={}&tbm=isch'.format(args[1])
    driver = webdriver.Chrome()
    driver.get(url)
    w = driver.execute_script('return document.body.scrollWidth')
    h = driver.execute_script('return document.body.scrollHeight')
    driver.set_window_size(w, h)
    driver.save_screenshot(image_filename)
    image_url = upload_image(image_filename)

    # make scrapbox page
    project_url = 'https://scrapbox.io/eda-englishwords/'
    make_scrapbox_page(project_url, args[1], image_url)


def upload_image(image_filename):
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


def make_scrapbox_page(project_url, english_word, image_url):
    image_tag = '[' + image_url + ']'

    scrapbox_url = project_url + english_word + '?body=' + image_tag
    subprocess.run(["open", scrapbox_url])


if __name__ == "__main__":
    main()
