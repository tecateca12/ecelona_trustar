'this file contains drivers to be selected after run tests'
from selenium import webdriver
from libs import builtins
import os

class chrome(object):
    def __init__(self):
        if builtins.VIRTUAL_DISPLAY:
            from pyvirtualdisplay import Display

            display = Display(visible=0, size=(
                builtins.BROWSER_WIDTH, builtins.BROWSER_HEIGHT))
            display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        if builtins.HEADLESS:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument(
            "--window-size={},{}".format(builtins.BROWSER_WIDTH, builtins.BROWSER_HEIGHT))
        self.driver = webdriver.Chrome(os.path.join(builtins.PROJECT_PATH,"libs","chromedriver"),options=chrome_options)
        self.driver.maximize_window()

def init_browser(browser):
    builtins.DRIVER = browser().driver

def quit_browser():
    builtins.DRIVER.quit()
