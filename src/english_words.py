#!/usr/bin/env python3
import sys
from selenium import webdriver


def main(args=sys.argv):
    # check arguments
    if len(args) == 1:
        print("Add it to the first argument.")
        sys.exit()

    # Google image search & save screenshot
    url = 'https://www.google.com/search?q={}&tbm=isch'.format(args[1])
    driver = webdriver.Chrome()
    driver.get(url)
    w = driver.execute_script('return document.body.scrollWidth')
    h = driver.execute_script('return document.body.scrollHeight')
    driver.set_window_size(w, h)
    driver.save_screenshot('screenshot.png')


if __name__ == "__main__":
    main()
