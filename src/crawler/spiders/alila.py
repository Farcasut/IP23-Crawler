import re
import scrapy
from itemloaders import ItemLoader
from scrapy import Selector
from ..items import Product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
class Alila(scrapy.Spider):
    name = 'Alila'
    start_urls = ['https://pizzeriaalila.ro/shop/']
    delivery_price = 0
    min_delivery = 30

    def parse(self, response):
        categories_pages = response.css('.category-grid-item .hover-mask .category-link-overlay::attr(href)').getall()
        for categorie_page in categories_pages:
            yield response.follow(categorie_page, callback=self.scrape_page  )


    def scrape_page(self, response):
        products = response.css('.product-title a::attr(href)').getall()
        for product in products:
            yield response.follow(product, callback= self.scrape_item)
    def scrape_item(self, response):
        l = ItemLoader(item=Product(), selector=response)
        l.add_value('restaurant_name', Alila.name)
        l.add_value('delivery_price', '0')
        l.add_value('min_delivery', '30')
        l.add_css('name', '.entry-title::text')
        l.add_value('source', 'site')
        l.add_css('price', '.basel-scroll-content bdi::text')
        l.add_css('images', 'figure a::attr(href)')
        l.add_css('category', '.posted_in a::text')
        l.add_css('description', '#tab-description p::text')
        yield l.load_item()
