import re
import scrapy
from itemloaders import ItemLoader
from scrapy import Selector

from .. import utils
from ..items import Product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


class CrawlerPhotos(scrapy.Spider):
    name = 'Photos'
    start_urls = ['https://images.google.com/']
    listOfNames = []

    def __init__(self):
        options = Options()
        options.add_argument('-headless')
        self.driver = webdriver.Firefox(options=options)
        self.pattern = re.compile(r'(https:.*\.jpg)')

    def getRestaurantsNames(self):
        query = " SELECT DISTINCT restaurant_data->'restaurant_name' FROM restaurants"
        connection = utils.create_db_connection();
        cursor = connection.cursor()
        cursor.execute(query)
        CrawlerPhotos.listOfNames = cursor.fetchall()
        cursor.close()
        connection.close()
    def insertRestaurantImages(self, tuples):
        query = "UPDATE restaurants SET restaurant_data = jsonb_set(restaurant_data, '{restaurant_image}', to_jsonb(?)) WHERE restaurant_data->>'restaurant_name' = ?"
        connection = utils.create_db_connection()
        cursor = connection.cursor()
        for restaurant_name, image in tuples:
            cursor.execute(query, (image, restaurant_name))
        connection.commit()
        cursor.close()
        connection.close()
    def getRestaurantsNames(self):
        query = " SELECT DISTINCT restaurant_data->'restaurant_name' FROM restaurants"
        connection = utils.create_db_connection();
        cursor = connection.cursor()
        cursor.execute(query)
        CrawlerPhotos.listOfNames = cursor.fetchall()
    def parse(self, response):
        self.driver.get(response.url)
        self.driver.implicitly_wait(60)
        #l=  ItemLoader(item=RestaurantImage())
        # Accept cookies
        accept_button = self.driver.find_element(By.CSS_SELECTOR, '.QS5gu.sy4vM')
        accept_button.click()
        items = []
        for names in  CrawlerPhotos.listOfNames:
            search_input = self.driver.find_element(By.CSS_SELECTOR, '#APjFqb')
            search_input.clear()
            search_input.send_keys(names+" restaurant iasi")
            search_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            search_button.click()
            self.driver.implicitly_wait(50)
            items.append((names,self.driver.find_elements(By.CSS_SELECTOR, '.rg_i.Q4LuWd')[0].get_attribute('src')))
            #l.add_value("name", names)
            #l.add_value("image_url", self.driver.find_elements(By.CSS_SELECTOR, '.rg_i.Q4LuWd')[0].get_attribute('src'))
            self.driver.back()
        self.insertRestaurantImages(items)

    def closed(self, reason):
        self.driver.quit()

