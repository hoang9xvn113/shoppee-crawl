


from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from time import sleep
import random
import pandas




class Product:
    def __init__(self, name, img, link, price) -> None:
        self.name = name
        self.price = price
        self.img = img
        self.link = link


class Laptop(Product):
    def __init__(self, name, screen, cpu, card, ram, disk, img, link, price) -> None:
        super().__init__(name, img, link, price)
        self.screen = screen
        self.cpu = cpu
        self.card = card
        self.ram = ram
        self.disk = disk


class Browser():
    executablePath = "chromedriver"
    headless = False

    def __init__(self, url) -> None:
        self.url = url

    def getOptions() -> Options:
        options = Options()
        options.headless = Browser.headless
        return options

    def getBrower(self) -> webdriver.Chrome:
        options = Browser.getOptions()
        browser = webdriver.Chrome(executable_path=Browser.executablePath, options=options)
        browser.maximize_window()
        browser.get(self.url)
        sleep(3)
        return browser

class LaptopXpath():
    count = 1


class LaptopCrawl():
    url = "https://fptshop.com.vn/may-tinh-xach-tay"
    currScroll = 1200

    def __init__(self):
        self.browser = Browser(LaptopCrawl.url).getBrower()

    def scrollPage(self):
        for i in range(1,10):
            LaptopCrawl.currScroll += 600
            self.browser.execute_script("window.scrollTo(0, {})".format(LaptopCrawl.currScroll))
            sleep(.5)

    def convertToExcel(data):
        myDataSet = {
            'name': [],
            'screen': [],
            'cpu': [],
            'card': [],
            'ram': [],
            'disk': [],
            'img': [],
            'link': [],
            'price': [],
        }

        for laptop in data:
            myDataSet['name'].append(laptop.name)
            myDataSet['screen'].append(laptop.screen)
            myDataSet['cpu'].append(laptop.cpu)
            myDataSet['card'].append(laptop.card)
            myDataSet['ram'].append(laptop.ram)
            myDataSet['disk'].append(laptop.disk)
            myDataSet['img'].append(laptop.img)
            myDataSet['link'].append(laptop.link)
            myDataSet['price'].append(laptop.price)
        
        myvar = pandas.DataFrame(myDataSet)
        myvar.to_excel('LaptopCrawl.xlsx')

    
    def crawl(self) -> list:
        laptops = []

        count = 1

        self.scrollPage()

        while(True):
            if (count>50):
                break

            if (count%20==0):
                btnXpath = '//*[@id="root"]/main/div/div[3]/div[2]/div[3]/div/div[3]/a'
                btnElement = self.browser.find_element_by_xpath(btnXpath)
                btnElement.click()
                sleep(3)
                self.scrollPage()


            
            nameXpath = '//*[@id="root"]/main/div/div[3]/div[2]/div[3]/div/div[2]/div[{}]/div[2]/h3/a'.format(count)
            priceXpath = '//*[@id="root"]/main/div/div[3]/div[2]/div[3]/div/div[2]/div[{}]/div[2]/div[1]/div[1]'.format(count)
            screenXpath = '//*[@id="root"]/main/div/div[3]/div[2]/div[3]/div/div[2]/div[{}]/div[2]/div[3]/div[1]/span[1]'.format(count)
            cpuXpath = '//*[@id="root"]/main/div/div[3]/div[2]/div[3]/div/div[2]/div[{}]/div[2]/div[3]/div[1]/span[2]'.format(count)
            ramXpath = '//*[@id="root"]/main/div/div[3]/div[2]/div[3]/div/div[2]/div[{}]/div[2]/div[3]/div[1]/span[3]'.format(count)
            diskXpath = '//*[@id="root"]/main/div/div[3]/div[2]/div[3]/div/div[2]/div[{}]/div[2]/div[3]/div[1]/span[4]'.format(count)
            cardXpath = '//*[@id="root"]/main/div/div[3]/div[2]/div[3]/div/div[2]/div[{}]/div[2]/div[3]/div[1]/span[5]'.format(count)
            imgXpath = '//*[@id="root"]/main/div/div[3]/div[2]/div[3]/div/div[2]/div[{}]/div[1]/a/span/img'.format(count)

            try:
                nameElement = self.browser.find_element_by_xpath(nameXpath)
                screenElement = self.browser.find_element_by_xpath(screenXpath)
                cpuElement = self.browser.find_element_by_xpath(cpuXpath)
                ramElement = self.browser.find_element_by_xpath(ramXpath)
                diskElement = self.browser.find_element_by_xpath(diskXpath)
                cardElement = self.browser.find_element_by_xpath(cardXpath)
                imgElement = self.browser.find_element_by_xpath(imgXpath)
                priceElement = self.browser.find_element_by_xpath(priceXpath)

                name = nameElement.text
                screen = screenElement.text
                cpu = cpuElement.text
                ram = ramElement.text
                disk = diskElement.text
                card = cardElement.text
                img = imgElement.get_attribute('src')
                link = nameElement.get_attribute('href')
                price = priceElement.text
                
                laptop = Laptop(name, screen, cpu, card, ram, disk, img, link, price)

                sleep(.2)

                laptops.append(laptop)
            except Exception:
                print("pass")
            finally:
                count += 1

 
        
        self.browser.close()

        return laptops

app = LaptopCrawl()
data = app.crawl()
LaptopCrawl.convertToExcel(data)





