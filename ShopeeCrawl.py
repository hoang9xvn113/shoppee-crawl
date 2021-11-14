
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from time import sleep
import random
import pandas



class Product():
    def __init__(self, name, price, quantitySold, address, link, img) -> None:
        self.name = name
        self.price = price
        self.quantitySold = quantitySold
        self.address = address
        self.link = link
        self.img = img

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

class ShopeeCrawl():
    currScroll = 600

    def __init__(self, url):
        self.browser = Browser(url).getBrower()

    def scrollPage(self):
        for i in range(1,10):
            ShopeeCrawl.currScroll += 500
            self.browser.execute_script("window.scrollTo(0, {})".format(ShopeeCrawl.currScroll))
            sleep(1)

    def convertToExcel(data, filename):
        myDataSet = {
            'name': [],
            'price': [],
            'quantitySold': [],
            'address': [],
            'link': [],
            'img': [],
        }

        for item in data:
            myDataSet['name'].append(item.name)
            myDataSet['price'].append(item.price)
            myDataSet['quantitySold'].append(item.quantitySold)
            myDataSet['address'].append(item.address)
            myDataSet['link'].append(item.link)
            myDataSet['img'].append(item.img)
        
        myvar = pandas.DataFrame(myDataSet)
        myvar.to_excel(filename)

    def mapping(self, count):
        nameXpath = '//*[@id="main"]/div/div[3]/div/div[4]/div[2]/div/div[2]/div[{}]/a/div/div/div[2]/div[1]/div[1]/div'.format(count)
        priceXpath = '//*[@id="main"]/div/div[3]/div/div[4]/div[2]/div/div[2]/div[{}]/a/div/div/div[2]/div[2]/div[2]/span[2]'.format(count)
        quantitySoldXpath = '//*[@id="main"]/div/div[3]/div/div[4]/div[2]/div/div[2]/div[{}]/a/div/div/div[2]/div[3]/div[3]'.format(count)
        addressXpath = '//*[@id="main"]/div/div[3]/div/div[4]/div[2]/div/div[2]/div[{}]/a/div/div/div[2]/div[4]'.format(count)
        imgXpath = '//*[@id="main"]/div/div[3]/div/div[4]/div[2]/div/div[2]/div[{}]/a/div/div/div[1]/img'.format(count)
        linkXpath = '//*[@id="main"]/div/div[3]/div/div[4]/div[2]/div/div[2]/div[{}]/a'.format(count)

        nameElement = self.browser.find_element_by_xpath(nameXpath)
        priceElement = self.browser.find_element_by_xpath(priceXpath)
        quantitySoldElement = self.browser.find_element_by_xpath(quantitySoldXpath)
        addressElement = self.browser.find_element_by_xpath(addressXpath)
        imgElement = self.browser.find_element_by_xpath(imgXpath)
        linkElement = self.browser.find_element_by_xpath(linkXpath)

        return {'nameElement': nameElement, 
                'priceElement': priceElement, 
                'quantitySoldElement': quantitySoldElement, 
                'addressElement': addressElement, 
                'imgElement': imgElement, 
                'linkElement': linkElement}
    
    def crawl(self):
        products = []

        count = 1

        page = 1

        maxPage = 5

        self.scrollPage()

        while(True):
            if (page>maxPage):
                break

            if (count>55):
                btnNextXpath = '//*[@id="main"]/div/div[3]/div/div[4]/div[2]/div/div[1]/div[2]/button[2]'
                btnNextElement = self.browser.find_element_by_xpath(btnNextXpath)
                btnNextElement.click()
                count = 1
                page += 1
                sleep(1)
                ShopeeCrawl.currScroll = 600
                self.scrollPage()

            try:
                elems = self.mapping(count)

                name = elems['nameElement'].text
                price = elems['priceElement'].text
                quantitySold = elems['quantitySoldElement'].text
                address = elems['addressElement'].text
                img = elems['imgElement'].get_attribute('src')
                link = elems['linkElement'].get_attribute('href')

                product = Product(name, price, quantitySold, address, link, img)

                products.append(product)
            except Exception:
                print("pass")
            finally:
                count += 1
        
        self.browser.close()

        return products


url = "https://shopee.vn/Nh%C3%A0-S%C3%A1ch-Online-cat.11036863?minPrice=60000&page=0"
app = ShopeeCrawl(url)
products = app.crawl()
print(len(products))
ShopeeCrawl.convertToExcel(products, 'ShopeeCrawl3.xlsx')




        








