

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from time import sleep
import random
import pandas

class Book():
    def __init__(self, name, publishing) -> None:
        pass



class Browser():
    executablePath = "chromedriver"


    def __init__(self, url) -> None:
        self.url = url

    def getOptions() -> Options:
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')


        return options

    def getBrower(self) -> webdriver.Chrome:
        options = Browser.getOptions()
        browser = webdriver.Chrome(executable_path=Browser.executablePath, options=options)
        browser.get(self.url)
        sleep(3)
        return browser