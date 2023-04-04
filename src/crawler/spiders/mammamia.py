import scrapy
from scrapy.http   import HtmlResponse
from scrapy.loader import ItemLoader

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options

from crawler.items import Product
from scrapy_selenium import Driver
from scrapy_selenium import SeleniumRequest
from crawler.spiders.abstractcrawler import AbstractCrawler

class MammaMia(AbstractCrawler):

    start_urls = [
                'https://www.mammamia.ro/menu'
            ]
    name = 'MammaMia'

    """
        The whole menu is displayed in a single page so link_selectors
        for the next page are not needed.
    """
    link_selectors = {}
    product_selectors = {"name" : ".cart-title::text", "description" : ".menufont::text", "price" : '.productPrice::text', 'images' : 'img::attr(data-src)'}

    default_product_values = {"restaurant_name" : "MammaMia", "source" : "site", "category" : "generic_category"}

    def __init__(self):
        pass

    def start_requests(self):
        self.setup()
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)
     
    def setup(self):
        """
            Make a selenium browser instance and set it to press the button for home delivery
        """
        self.driver = Driver().get_instance() # Get the Singleton Driver instance
        self.driver.get(self.start_urls[0])   # Go to the page
        lirare_btn = self.driver.find_element(By.CLASS_NAME, 'btn') # Get the home delivery button
        lirare_btn.click() # Press it

    def parse(self, response : HtmlResponse):
        for product in response.css('.productCard'):
            yield self.helper_get_product(response=response, selector=product)
