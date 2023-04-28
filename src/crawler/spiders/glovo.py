import scrapy
from scrapy.loader import ItemLoader
from scrapy import Request

from crawler.utils import get_rid_of_special_spaces
from crawler.items import Product

class Glovo(scrapy.Spider):
    name = "Glovo"
    start_urls = [
            "https://glovoapp.com/ro/en/iasi/restaurants_1/"
    ]
    

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url = url, callback = self.parse)

    def parse(self, response : scrapy.http.HtmlResponse):
        for restaurant in response.css('.collection-item::attr(href)').getall():
            yield response.follow(str(restaurant), callback=self.parse_restaurant)
        
        if len(response.css('.next-page-link::attr(href)')) > 0:
            next_page = response.css('.next-page-link::attr(href)').get()
            yield response.follow(str(next_page), callback=self.parse)
    
    def parse_restaurant(self, response):
        if len(response.css('.card__link')) > 0:
            for card_link in response.css('.card__link::attr(href)').getall():
                if card_link != None:
                   yield response.follow(str(card_link), callback=self.parse_restaurant) 
        elif len(response.css('.list')) > 0:
            selectors = {'restaurant_name': 'h1::text', 'categories': '.list', 'category': 'div > p::text',
                         'products': '.product-row', 'product_name': '.product-row__name span::text',
                         'product_description': '.product-row__info__description span::text', 
                         'product_price': '.product-price span::text', 'product_image': '.product-row__image::attr(src)'
                         }
            for generated in self.parse_page_of_restaurant(response, selectors):
                yield generated
        elif len(response.css('.carousel')) > 0:
            selectors = {'restaurant_name': 'h1::text', 'categories': '.store__body__dynamic-content', 'category': 'div > p::text',
                         'products': '.carousel__content__element', 'product_name': '.tile__description span::text',
                         'product_description': '.tile__description span::text', 
                         'product_price': '.product-price span::text', 'product_image': '.store-product-image::attr(src)'
                         }
            for generated in self.parse_page_of_restaurant(response, selectors):
                yield generated
            
            for page in response.css('.tile'):
                next_page = page.css('a::attr(href)').getall()
                if next_page != None:
                    for link in next_page:
                        yield response.follow(str(link), callback=self.parse_carousel_restaurant_subpages)


    def parse_page_of_restaurant(self, response, selectors):
        restaurant_name = response.css(selectors['restaurant_name']).get()
        if restaurant_name != None:
            restaurant_name = restaurant_name.strip()
        for category_list in response.css(selectors['categories']):
            category_name = category_list.css(selectors['category']).get()
            for product in category_list.css(selectors['products']):
                item = ItemLoader(item=Product(), response=response, selector=product)
                
                product_name = product.css(selectors['product_name']).get().strip()
                product_description = product.css(selectors['product_description']).get()
                product_price = get_rid_of_special_spaces(product.css(selectors['product_price']).get())
                
                item.add_value('images', self.get_product_image(selectors['product_image'], product))
                
                if category_name != None:
                    item.add_value('category', category_name.strip())
                
                if product_description != None:
                    item.add_value('description', product_description.strip())

                item.add_value('restaurant_name', restaurant_name)
                item.add_value('name', product_name)
                item.add_value('price', product_price)
                item.add_value('source', Glovo.name)
                yield item.load_item()
      
    def parse_carousel_restaurant_subpages(self, response):
        restaurant_name = response.css('h1::text').get()
        if restaurant_name != None:
            restaurant_name = restaurant_name.strip()
        for category_list in response.css('.grid'):
            category_name = category_list.css("h2::text").get()
            for product in category_list.css('.tile'):
                item = ItemLoader(item=Product(), response=response, selector=product)
                product_name = product.css('.tile__description span::text').get().strip()
                product_price = get_rid_of_special_spaces(product.css('.product-price span::text').get())

                item.add_value('images', self.get_product_image('.store-product-image::attr(src)', product))

                if category_name != None:
                    item.add_value('category', category_name.strip())
 
                item.add_value('restaurant_name', restaurant_name)
                item.add_value('name', product_name)
                item.add_value('price', product_price)
                item.add_value('source', Glovo.name)
                yield item.load_item()
    
    high_res_images = "https://res.cloudinary.com/glovoapp/w_600,f_auto,q_auto/Products/"
    def get_product_image(self, selector, product):
        image_name = product.css(selector).get()
        product_image = image_name
        if image_name != None:
            if 'cloudinary.com/glovoapp' in image_name:
                image_name = image_name.split('/')[-1]
                product_image = self.high_res_images + image_name
        else:
            product_image = ''
        return product_image

