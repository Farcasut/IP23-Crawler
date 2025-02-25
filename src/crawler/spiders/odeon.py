import re

import scrapy
from itemloaders import ItemLoader
from ..items import Product
from crawler.utils import get_rid_of_special_spaces

class Odeon(scrapy.Spider):
    name = 'Odeon'
    start_urls = ['https://www.restaurantodeon.ro/magazin/']

    def parse(self, response):
        next_page=response.css('.next::attr(href)').get()
        product_pages = response.css('.red::attr(href)').getall()
        for product_page in product_pages:
            yield response.follow(product_page, callback=self.scrape_item)
        if next_page is not None:
            yield response.follow(next_page, self.parse)
            
    def scrape_item(self, response):
        l = ItemLoader(item=Product(), selector=response)
        l.add_value('restaurant_name', Odeon.name)
        l.add_value('delivery_price', '0')
        l.add_value('min_delivery', '40')
        l.add_css('name', '#content .title::text')
        l.add_value('source', 'site')
        l.add_css('price', 'meta[property="product:price:amount"]::attr(content)'),
        l.add_css('images', '.attachment-shop_single::attr(src)')
        l.add_css('category', '.posted_in atext')
        description = response.css('.ingrediente p::text').get()
        if description is not None:
            l.add_value('description', description)
        else:
            l.add_value('description', ' ')
        yield l.load_item()
