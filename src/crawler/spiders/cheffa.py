import re
import scrapy
from itemloaders import ItemLoader
from scrapy import Selector
from ..items import Product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
class Cheffa(scrapy.Spider):
    name = 'Cheffa'
    start_urls = ['https://www.cheffa.ro/']


    def parse(self, response):
        category_pages = response.css('.menu-drop.__GomagMM a::attr(href)').getall()
        category = response.css('.menu-drop.__GomagMM a::attr(title)').getall();
        for pair in zip(category_pages, category):
            yield response.follow(pair[0], callback=self.scrape_page, cb_kwargs={'category': pair[1]})

    def scrape_page(self, response, category):
        products  = response.css('.image-holder a::attr(href)').getall()
        for product in products:
            yield response.follow(product,callback=self.scrape_item, cb_kwargs={'category':category})


    def scrape_item(self, response,category):
        l = ItemLoader(item=Product(), selector=response)
        l.add_value('restaurant_name', Cheffa.name)
        l.add_value('name',  response.css('.title span::text').get().strip())
        l.add_value('source', 'site')
        l.add_value('price', response.css('.detail-price.text-main .fPrice::text').get().strip())
        l.add_value('images', response.css('link[rel="preload"]::attr(href)').get())
        l.add_value('category', category)
        l.add_css('description', '.short-description div::text')
        yield l.load_item()
