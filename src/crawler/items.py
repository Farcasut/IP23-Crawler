import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst
from scrapy import Field
import re

from crawler.utils import get_rid_of_special_spaces

def convert_to_float(input_str):
    input_str.replace(',', '.')
    number = ''
    for char in input_str:
        if char.isdigit() or char == '.':
            number += char
        elif number:
            break
    if number == '':
        return ''
    return float(number)

class Product(scrapy.Item):
    restaurant_name = scrapy.Field(input_processor = MapCompose(get_rid_of_special_spaces), output_processor = TakeFirst())
    source          = scrapy.Field(input_processor = MapCompose(get_rid_of_special_spaces), output_processor = TakeFirst())
    name            = scrapy.Field(input_processor = MapCompose(get_rid_of_special_spaces), output_processor = TakeFirst()) 
    category        = scrapy.Field(input_processor = MapCompose(get_rid_of_special_spaces), output_processor = TakeFirst()) 
    description     = scrapy.Field(input_processor = MapCompose(get_rid_of_special_spaces), output_processor = TakeFirst()) 
    price           = scrapy.Field(input_processor = MapCompose(convert_to_float), output_processor = TakeFirst()) # float price
    images          = scrapy.Field() # list of images in the given path
    delivery_price  = scrapy.Field(input_processor = MapCompose(convert_to_float), output_processor = TakeFirst()) #only the price for delivery
    min_delivery    = scrapy.Field(input_processor = MapCompose(convert_to_float), output_processor = TakeFirst()) #minimum delvery that you need to fufill
