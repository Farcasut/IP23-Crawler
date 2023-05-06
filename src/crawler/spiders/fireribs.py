import re

import scrapy
from itemloaders import ItemLoader

from crawler.items import Product
from crawler import utils

class FireRibs(scrapy.Spider):
    name='FireRibs'
    start_urls = [
    'https://fire-ribs.ro/meniu/'
    ]

    def parse(self, response):
        category_pages=response.css('#woocommerce_product_categories-13 a::attr(href)').getall()
        product_category=response.css('#woocommerce_product_categories-13 a::text').getall()
        for pair in zip(category_pages, product_category):
            yield response.follow(pair[0], callback=self.scrape_category, cb_kwargs={'category': pair[1]})

    def scrape_category(self, response, category):
        products = response.css('.woocommerce-loop-product__link::attr(href)').getall()
        for product in products:
            yield response.follow(product, callback=self.scrape_item,cb_kwargs={'category': category})

    def scrape_item(self, response, category):
        l = ItemLoader(item=Product(), selector=response)
        l.add_value('restaurant_name', 'Fire Ribs')
        l.add_value('source', 'site')
        l.add_value('category', category)
        l.add_value('name', response.css('.entry-title::text').get().strip())
        l.add_value('description', ''.join(response.css('#tab-description p::text').getall()))
        l.add_css('price', 'p.price.product-page-price span.woocommerce-Price-amount.amount bdi::text')
        l.add_css('images', '.skip-lazy::attr(src)')
        yield l.load_item()
