import re
import scrapy
from itemloaders import ItemLoader
from scrapy import Selector
from ..items import Product
from selenium import webdriver
from selenium.webdriver.common.by import By

class Vivo(scrapy.Spider):
    name = 'Vivo'
    start_urls = ['https://www.foodbooking.com/ordering/restaurant/menu?restaurant_uid=7254b63a-69e7-462d-be57-0b2505ab14a6']

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.pattern =  re.compile(r'(https:.*\.jpg)')

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.implicitly_wait(60)

        products = self.driver.find_elements(By.CLASS_NAME, 'm-item-container')
        for product in products:
            outerHTML = product.get_attribute('outerHTML')
            sel  = Selector(text=outerHTML)
            text_file = open(".pizdamasii", "w")
            text_file.write(outerHTML)
            yield from self.scrape_item(sel)

    def scrape_item(self, selector):
        l = ItemLoader(item=Product(), selector=selector)
        l.add_value('restaurant_name', Vivo.name)
        l.add_css('name', '.m-item-name::text')
        l.add_value('source', 'site')
        l.add_css('price', '.m-item-price span::text')
        url = selector.css('.m-item-picture::attr(style)').get()
        if url is not None:
            l.add_value('images',  self.pattern.findall(url)[0])
        else:
            l.add_value('images', ' ')
        l.add_value('category', '')
        description = selector.css('.m-item-description::text').get()
        if description is not None:
            l.add_value('description', description.strip())

        yield l.load_item()
