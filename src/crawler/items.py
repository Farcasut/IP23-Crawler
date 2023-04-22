import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst
from scrapy import Field
import re


def convert_to_float(input_str):
    input_str.replace(',', '.')
    numberOnly = [float(s) for s in re.findall(r'\d+\.?\d*', input_str)]
    return numberOnly

class Product(scrapy.Item):
    restaurant_name = scrapy.Field(output_processor = TakeFirst())
    source          = scrapy.Field(output_processor = TakeFirst())
    name            = scrapy.Field(output_processor = TakeFirst()) 
    category        = scrapy.Field(output_processor = TakeFirst()) 
    description     = scrapy.Field(output_processor = TakeFirst()) 
    price           = scrapy.Field(input_processor = MapCompose(convert_to_float), output_processor = TakeFirst()) # float price
    images          = scrapy.Field() # list of images in the given path
