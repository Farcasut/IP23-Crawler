import scrapy

class Product(scrapy.Item):
    restaurant_name = scrapy.Field()
    source          = scrapy.Field()
    name            = scrapy.Field() 
    category        = scrapy.Field() 
    description     = scrapy.Field() 
    price           = scrapy.Field() # float price
    images          = scrapy.Field() # list of images in the given path
