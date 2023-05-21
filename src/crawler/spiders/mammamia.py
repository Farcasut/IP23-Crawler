import scrapy
from scrapy.http   import HtmlResponse
from scrapy.loader import ItemLoader
from scrapy import Request

from selenium.webdriver.common.by import By

from crawler.items import Product
from crawler.utils import SeleniumRequest
from crawler.utils import create_selenium_driver

import sys

class MammaMia(scrapy.Spider):

    start_urls = [
                'https://www.mammamia.ro/menu'
            ]
    name = 'MammaMia'

    def __init__(self):
        self.driver = create_selenium_driver() 
        self.driver.get(self.start_urls[0]) 
        lirare_btn = self.driver.find_element(By.CLASS_NAME, 'btn')
        lirare_btn.click()

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response : HtmlResponse):
        category_list = response.css('.col-md-12')
        for i in range(1, len(category_list), 2):
            category_name = category_list[i].css('h5::text').get()
            for product in category_list[i+1].css('.productCard'):
                item = ItemLoader(item=Product(), response=response, selector=product)
                item.add_value("restaurant_name", "Mamma Mia")
                item.add_value('delivery_price', '0')
                item.add_value('min_delivery', '50')
                item.add_value('source', 'site')
                item.add_value('category', category_name)
                item.add_css('name', '.card-title::text')
                item.add_css('description', '.menufont::text')
                item.add_css('price', '.productPrice::text')
                item.add_css('images', 'img::attr(data-src)')

                yield item.load_item()


