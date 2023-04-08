import re

import scrapy
from itemloaders import ItemLoader

from ..items import Product
from crawler import utils

class Tazz(scrapy.Spider):
    name = 'Tazz'
    start_urls = [
        'https://tazz.ro/iasi/restaurante'
    ]

    def parse(self, response):
        restaurants_pages = response.css('.partnersListLayout a::attr(href)').getall()

        for restaurant_page in restaurants_pages:
            yield response.follow(restaurant_page, callback=self.scrape_restaurant)


    def process_prices(self, response):
        r = re.compile(
            '(<span class=\"price-container zprice\">(\d*) <sup> (\d*)<\/sup> </span>)|(<span '
            'class=\"price-container\">(\w*)</span>)|(<span class=\"product-price promo zprice\">(\d*) <sup> ('
            '\d*)</sup> </span>)')
        prices = []
        for i in response.css('.price-container , .promo').getall():
            result = r.match(i)
            if result is not None and result.group(2) is not None:
                prices.append(result.group(2) + '.' + result.group(3))
            elif result is not None and result.group(7) is not None:
                prices.append(result.group(7) + '.' + result.group(8))
            else:
                # for the out-of-stock products
                prices.append(-1)
        return prices


    def process_images(self, response):
        images=[]
        for i in response.css('.restaurant-product-card').getall():
            start_index =  i.find('img src=')
            if start_index==-1:
                images.append('')
                continue
            start_quotes = i.find('"', start_index)
            end_quotes = i.find('"', start_quotes+1)
            images.append(i[start_quotes+1:end_quotes])
        return images

    def scrape_restaurant(self, response):
        prices = self.process_prices(response)
        product_titles = response.css('.title-container::text').getall()
        product_descriptions = response.css('.description-container::text').getall();
        current_restaurant = response.css('.tb_partner_name::text').get()
        images=self.process_images(response)
        deals = []
        for i in zip(product_titles, product_descriptions, prices, images):
            if i[2] != -1 and i[0] not in deals:
                if "reducere" in i[0]:
                    deals.append(" ".join(i[0].split(' ')[2:]))
                l = ItemLoader(item=Product(), selector=response)
                l.add_value('restaurant_name', current_restaurant.strip())
                l.add_value('source', Tazz.name)
                l.add_value('category', '')
                l.add_value('name', i[0].strip())
                l.add_value('description', utils.get_rid_of_special_spaces(i[1]))
                l.add_value('price', i[2])
                l.add_value('images', i[3])
            else:
                continue
            yield l.load_item()
