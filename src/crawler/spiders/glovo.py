import scrapy
from scrapy.loader import ItemLoader
from scrapy import Request
from scrapy_selenium import Driver
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from urllib.parse import urlparse

from crawler.utils import extract_domain
from crawler.utils import get_rid_of_special_spaces
from crawler.items import Product

class Glovo(scrapy.Spider):
    name = "Glovo"
    start_urls = [
#            "https://glovoapp.com/ro/en/iasi/tiki-bistro-ias",
#             "https://glovoapp.com/ro/en/iasi/kfc-ias/",
#            "https://glovoapp.com/ro/en/iasi/icecreamloveias/",
#            "https://glovoapp.com/ro/en/iasi/the-box-iasi/",
#            "https://glovoapp.com/ro/en/iasi/torro-burgers/",
            "https://glovoapp.com/ro/en/iasi/restaurants_1/"
            ]
    
    images = "https://res.cloudinary.com/glovoapp/w_600,f_auto,q_auto/Products/"

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url = url, callback = self.parse)

    def parse(self, response : scrapy.http.HtmlResponse):
        for restaurant in response.css('.collection-item::attr(href)').getall():
            yield response.follow(str(restaurant), callback=self.parse_restaurant)
        
        if len(response.css('.next-page-link::attr(href)')) > 0:
            print("A"*1500)
            next_page = response.css('.next-page-link::attr(href)').get()
            yield response.follow(str(next_page), callback=self.parse)
    
    def parse_restaurant(self, response):
        if len(response.css('.card__link')) > 0:
            for card_link in response.css('.card__link::attr(href)').getall():
                if card_link != None:
                   yield response.follow(str(card_link), callback=self.parse_restaurant) 
        elif len(response.css('.list')) > 0:
            for generated in self.parse_normal_restaurant(response):
                yield generated
        elif len(response.css('.carousel')) > 0:
            for generated in self.parse_carousel_restaurant(response):
                yield generated
       
    def parse_normal_restaurant(self, response):
        restaurant_name = response.css('h1::text').get()
        if restaurant_name != None:
            restaurant_name = restaurant_name.strip()
        for category_list in response.css('.list'):
            category_name = category_list.css("div > p::text").get()
            for product in category_list.css('.product-row'):
                item = ItemLoader(item=Product(), response=response, selector=product)
                product_name = product.css('.product-row__name span::text').get().strip()
                product_description = product.css('.product-row__info__description span::text').get()
                product_price = get_rid_of_special_spaces(product.css('.product-price span::text').get())
                
                image_name = product.css('.product-row__image::attr(src)').get()
                if image_name != None:
                    if 'cloudinary' in image_name:
                        image_name = image_name.split('/')[-1]
                        product_image = self.images + image_name
                    else:
                        product_image = image_name
                   
                    item.add_value('images', product_image)
                
                if category_name != None:
                    item.add_value('category', category_name.strip())
                
                if product_description != None:
                    item.add_value('description', product_description.strip())

                item.add_value('restaurant_name', restaurant_name)
                item.add_value('name', product_name)
                item.add_value('price', product_price)

                yield item.load_item()


    def parse_carousel_restaurant(self, response):
        restaurant_name = response.css('h1::text').get()
        if restaurant_name != None:
            restaurant_name = restaurant_name.strip()
        for category_list in response.css('.store__body__dynamic-content'):
            category_name = category_list.css("div > h2::text").get()
            for product in category_list.css('.carousel__content__element'):
                item = ItemLoader(item=Product(), response=response, selector=product)
                product_name = product.css('.tile__description span::text').get().strip()
                product_price = get_rid_of_special_spaces(product.css('.product-price span::text').get())
                
                image_name = product.css('.store-product-image::attr(src)').get()
                if image_name != None:
                    if 'cloudinary' in image_name:
                        image_name = image_name.split('/')[-1]
                        product_image = self.images + image_name
                    
                    item.add_value('images', product_image)
                
                if category_name != None:
                    item.add_value('category', category_name.strip())
                
                item.add_value('restaurant_name', restaurant_name)
                item.add_value('name', product_name)
                item.add_value('price', product_price)

                yield item.load_item()

        for page in response.css('.tile'):
            next_page = page.css('a::attr(href)').getall()
            if next_page != None:
                yield response.follow(str(next_page), callback=self.parse_carousel_restaurant_subpages)
      
    def parse_carousel_restaurant_subpages(self, response):
        restaurant_name = response.css('.store-info__title::text').get()
        if restaurant_name != None:
            restaurant_name = restaurant_name.strip()
        for category_list in response.css('.store__body__dynamic-content'):
            category_name = category_list.css("div > h2::text").get()
            for product in category_list.css('.tile'):
                item = ItemLoader(item=Product(), response=response, selector=product)
                product_name = product.css('.tile__description span::text').get().strip()
                product_price = get_rid_of_special_spaces(product.css('.product-price span::text').get())
                
                image_name = product.css('.store-product-image::attr(src)').get()
                if image_name != None:
                    if 'cloudinary' in image_name:
                        image_name = image_name.split('/')[-1]
                        product_image = self.images + image_name
                    
                    item.add_value('images', product_image)
                
                if category_name != None:
                    item.add_value('category', category_name.strip())
                
                item.add_value('restaurant_name', restaurant_name)
                item.add_value('name', product_name)
                item.add_value('price', product_price)

                yield item.load_item()

