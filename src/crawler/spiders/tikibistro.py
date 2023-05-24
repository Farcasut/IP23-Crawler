import re
import scrapy
from itemloaders import ItemLoader
from scrapy import Selector
from ..items import  Product
from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from crawler.utils import create_selenium_driver

class TikiBistro(scrapy.Spider):
    name = 'TikiBistro'
    start_urls = ['https://delivery.tikibistro.ro/meniu']

    def __init__(self):
        self.driver = create_selenium_driver() 
        self.pattern = re.compile(r'(https:.*\.jpg)')



    def parse(self, response):
        self.driver.get(response.url)
        self.driver.implicitly_wait(30)
        categories = self.driver.find_elements(By.CLASS_NAME, 'padding_text_container')
        for category in categories:
            category_name = category.find_element(By.CLASS_NAME, 'text_container')
            products = category.find_elements(By.CLASS_NAME, 'box_produs')
            for product in products:
                outerHTML = product.get_attribute('outerHTML')
                sel = Selector(text= outerHTML)
                yield from self.scrape_item(sel, category.text)

        self.driver.close()


    def scrape_item(self, selector, category):
        l = ItemLoader(item = Product(), selector = selector)
        l.add_value('restaurant_name', 'Tiki Bistro')
        l.add_css('name', '.titlu_box::text')
        l.add_value('delivery_price', '12')
        l.add_value('min_delivery', '50')
        l.add_value('source', 'site')
        l.add_css('price','.pret_box::text')
        l.add_css('images', 'img::attr(data-src)')
        l.add_value('category', category)
        l.add_css('description','.descriere_box::text')

        yield l.load_item()

