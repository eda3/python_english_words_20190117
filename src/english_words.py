#!/usr/local/bin/python3

import json
import os
import platform
import re
import subprocess
import sys

from gyazo import Api
from selenium import webdriver


def main(args=sys.argv):
    # Check arguments
    if len(args) == 1:
        print("Enter the first argument.")
        sys.exit()

    # Look up English meaning
    search_word = args[1]
    meanings = ""

    # Google image search & save screenshot
    image_filename = "screenshot.png"
    url = "https://www.google.com/search?q={}&tbm=isch".format(search_word)
    driver = webdriver.Chrome()
    driver.get(url)
    w = driver.execute_script("return document.body.scrollWidth")
    h = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(w, h)
    driver.save_screenshot(image_filename)
    image_url = __upload_image(image_filename)

    # Make scrapbox page
    project_url = "https://scrapbox.io/eda-englishwords/"
    __make_scrapbox_page(project_url, search_word, image_url, meanings)


def __upload_image(image_filename):
    if "API_TOKEN" not in os.environ:
        print("command `export API_TOKEN=hoge`")

    API_TOKEN = os.environ.get("API_TOKEN")
    client = Api(access_token=API_TOKEN)

    # Upload an image
    with open(image_filename, "rb") as f:
        image = client.upload_image(f)
        image_json = image.to_json()
        image_dict = json.loads(image_json)
        image_url = image_dict["url"]

    return image_url


def __make_scrapbox_page(project_url, english_word, image_url, meanings):
    image_tag = "[" + image_url + "]"

    scrapbox_url = project_url + english_word
    scrapbox_url += "?body="
    for meaning in meanings:
        scrapbox_url += "[[" + meaning + "]]" + "_____"
    scrapbox_url += image_tag

    # Delete character reference(e.g. &nbsp;)
    scrapbox_url = re.sub(r"&.*;", "", scrapbox_url)

    scrapbox_url = '"' + scrapbox_url + '"'
    cmd = "open " + scrapbox_url
    subprocess.check_call(cmd, shell=True)

    print("end")

    # Mac限定
    pf = platform.system()
    if pf == "Darwin":
        subprocess.run(["say", english_word])


if __name__ == "__main__":
    if True:
        main()
