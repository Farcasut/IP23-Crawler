import re

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.chrome.webdriver import WebDriver
from crawler.pipelines import DownloadImages
import json
from .. import utils


class CrawlerPhotos(scrapy.Spider):
    name = 'RestaurantPhotos'
    start_urls = ['https://images.google.com/']
    listOfNames = []

    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        self.driver = WebDriver(options=options)
        self.pattern = re.compile(r'(https:.*\.jpg)')
        self.downloader = DownloadImages()
        self.getRestaurantsNames()

    def getRestaurantsNames(self):
        query = "SELECT DISTINCT restaurant_data->>'restaurant_name' FROM restaurants"
        connection = utils.create_db_connection();
        cursor = connection.cursor()
        cursor.execute(query)
        CrawlerPhotos.listOfNames = cursor.fetchall()
        CrawlerPhotos.listOfNames = [i[0] for i in CrawlerPhotos.listOfNames]
        cursor.close()
        connection.close()

    def insertRestaurantImages(self, tuples):
        query = "UPDATE restaurants SET restaurant_data = jsonb_set(restaurant_data, '{restaurant_image}', %s) WHERE restaurant_data->>'restaurant_name' = %s"
        connection = utils.create_db_connection()
        cursor = connection.cursor()
        for restaurant_name, image in tuples:
            cursor.execute(query, (json.dumps(image), restaurant_name))
        connection.commit()
        cursor.close()
        connection.close()
   
    def uploadImagesToS3(self, tuples):
        new_tuples = []
        for i in range(len(tuples)):
            resulted_image = self.downloader.download_image(self, tuples[i][1])
            if resulted_image is not None:
                new_tuples.append((tuples[i][0], resulted_image))
        return new_tuples
            

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.implicitly_wait(60)
        # Accept cookies
        accept_button = self.driver.find_element(By.CSS_SELECTOR, '.QS5gu.sy4vM')
        accept_button.click()
        items = []
        for names in CrawlerPhotos.listOfNames:
            search_input = self.driver.find_element(By.CSS_SELECTOR, '#APjFqb')
            search_input.clear()
            search_input.send_keys(names + " restaurant iasi")
            search_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            search_button.click()
            self.driver.implicitly_wait(50)
            items.append((names, self.driver.find_elements(By.CSS_SELECTOR, '.rg_i.Q4LuWd')[0].get_attribute('src')))
            self.driver.back()
        items = self.uploadImagesToS3(items)
        self.insertRestaurantImages(items)

    def closed(self, reason):
        self.driver.quit()
