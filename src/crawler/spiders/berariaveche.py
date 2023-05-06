import re
import scrapy
from itemloaders import ItemLoader
from scrapy import Selector
from ..items import Product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
class BerariaVeche(scrapy.Spider):
    name = 'BerariaVeche'
    start_urls = ['https://berariavecheiasi.poloniq.ro/']

    def __init__(self):
        options = Options()
        options.add_argument('-headless')
        self.driver = webdriver.Firefox(options=options)


    def parse(self, response):
        self.driver.get(response.url)
        self.driver.implicitly_wait(60)

        products = self.driver.find_elements(By.CLASS_NAME, 'command_menu_list_item_column')
        descriptions = self.driver.find_elements(By.CLASS_NAME, 'command_menu_list_item_desc')
        for product in zip(products, descriptions):
            outerHTML = product[0].get_attribute('outerHTML')
            sel = Selector(text=outerHTML)
            yield from self.scrape_item(sel, product[1])
        self.driver.close()


    def scrape_item(self, selector, description):
        l = ItemLoader(item=Product(), selector=selector)
        l.add_value('restaurant_name', 'Beraria Veche')
        l.add_css('name', '.command_menu_list_item_title::text')
        l.add_value('source', 'site')
        l.add_css('price', '.command_menu_list_item_price::text')
        l.add_css('images',  '.obj_fit_img::attr(src)')
        l.add_value('category', '')
        l.add_value('description', description.text.replace('\n',' '))
        yield l.load_item()
