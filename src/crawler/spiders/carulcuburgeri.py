import time
import scrapy
from itemloaders import ItemLoader
from scrapy import Selector
from ..items import Product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from crawler.utils import create_selenium_driver


class CarulCuBurgeri(scrapy.Spider):
    name = 'CarulCuBurgeri'
    start_urls = ['https://carulcuburgeri.ro']

    def __init__(self):
        self.driver = create_selenium_driver()

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.implicitly_wait(60)
        categories = self.driver.find_elements(By.TAG_NAME, 'hrc-image-category-card')
        for category in categories:
            outerHTML = category.get_attribute('outerHTML')
            sel = Selector(text=outerHTML)
            new_tab = self.driver.execute_script("window.open('');")  # Open a new tab
            self.driver.switch_to.window(self.driver.window_handles[-1])  # Switch to the new tab
            yield from self.scrape_page(CarulCuBurgeri.start_urls[0] + sel.css('a::attr(href)').get(),
                                        sel.css('.category-name::text').get())
            self.driver.close()  # Close the new tab and switch back to the initial one
            self.driver.switch_to.window(self.driver.window_handles[0])
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            self.driver.close()

    def scrape_page(self, page_link, category):
        self.driver.get(page_link)
        self.driver.implicitly_wait(60)
        products = self.driver.find_elements(By.CLASS_NAME, 'col-lg-4')
        for product in products:
            outerHTML = product.get_attribute('outerHTML')
            sel = Selector(text=outerHTML)

            script_js = """
                var something = document.querySelector("ion-img");
                if (something !== null) { 
                    return something.shadowRoot.querySelector("img");
                }
                return "";
            """

            shadow_root = self.driver.execute_script(script_js, product)
            image = ""
            if shadow_root is not None and shadow_root is not "":
                image = shadow_root.get_attribute('src')
            yield from self.scrape_item(sel, category, image)

    def scrape_item(self, sel, category, image_url):
        l = ItemLoader(item=Product(), selector=sel)
        l.add_value('restaurant_name', CarulCuBurgeri.name)
        l.add_css('name', '.text-capitalize::text')
        l.add_value('source', 'site')
        l.add_value('images', image_url)
        if category not in ["Sosuri", "Bauturi"]:
            l.add_css('price', 'div.product-details-card .prod-price > div:nth-child(1)::text')
        else:
            l.add_css('price', ".product-container .divider-container .prod-price.d-flex div::text")
        l.add_value('category', category)
        l.add_css('description', ".details::text")
        yield l.load_item()
