import re

import scrapy
from itemloaders import ItemLoader
from scrapy import Selector
from ..items import Product

class Krud (scrapy.Spider):
    name = 'Krud'
    start_urls = ['https://www.krud.ro/meniu/']

    def parse(self, response):
        products = response.css('.zn-priceList-itemRight').getall()
        for product in products:
            yield self.scrape_item(product)

    def scrape_item(self, product):
        element = Selector(text=product)
        l = ItemLoader(item=Product(), selector=element)
        l.add_value('restaurant_name', Krud.name)
        l.add_value('delivery_price', '15')
        l.add_value('min_delivery', '0')
        l.add_css('name', '.zn-priceList-itemTitle::text')
        l.add_value('source', 'site')
        l.add_css('price', '.zn-priceList-itemPrice::text'),
        l.add_value('images', '')
        l.add_value('category', '')
        l.add_css('description', '.zn-priceList-itemDesc::text')
        return  l.load_item()