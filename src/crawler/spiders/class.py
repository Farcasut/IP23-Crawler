import re
import scrapy
from itemloaders import ItemLoader
from scrapy import Selector
from ..items import Product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
class Class(scrapy.Spider):
    name = 'Class'
    start_urls = ['https://www.classiasi.ro/']


    def parse(self, response):
        products = response.css('.nivel_2_li a::attr(href)').getall()
        for product in products:
            yield response.follow(product, callback=self.scrape_item)


    def scrape_item(self, response):
        l = ItemLoader(item=Product(), selector=response)
        l.add_value('restaurant_name', Class.name)
        l.add_value('delivery_price', '0')
        l.add_value('min_delivery', '40')
        l.add_css('name', '.col-md-7.col-sm-6 .title::text')
        l.add_value('source', 'site')
        l.add_css('price', '#pret_total::text')

        image_url= r'https://www.classiasi.ro/' + response.css('.ex1 img::attr(src)').get()
        l.add_value('images', image_url)
        l.add_value('category', '')
        l.add_value('description', ' '.join(response.css('.ingrediente li::text').getall()).replace('\r', ''))
        yield l.load_item()
