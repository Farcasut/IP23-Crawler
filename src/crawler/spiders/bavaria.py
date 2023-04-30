import scrapy

from itemloaders import ItemLoader
from ..items import Product
from crawler import utils

from scrapy import Selector

class Bavaria(scrapy.Spider):
    name = 'Bavaria'
    start_urls = [
        'https://www.bavariaiasi.ro/menu/'
    ]

    def parse(self, response):
        products = response.css(
            '.food-list-wrapper').getall()
        #print(products)
        for product in products:
            yield self.scrape_item(product)

    def scrape_item(self, product):
        element = Selector(text=product)
        l = ItemLoader(item=Product(), selector=element)
        l.add_value('restaurant_name', Bavaria.name)
        l.add_css('name', '.food-list-title a::text')
        l.add_value('source', 'site')
        l.add_css('price', '.food-price::text')
        l.add_value('images', utils.check_existance(element.css('.gdl-image a::attr(href)').get()))
        l.add_value('category', ' ')
        l.add_value('description', utils.check_existance(element.css('.food-list-excerpt::text').get()))
        return l.load_item()