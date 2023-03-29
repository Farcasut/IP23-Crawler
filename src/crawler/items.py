import scrapy

class Product(scrapy.Item):
    restaurant_name     = scrapy.Field()
    source              = scrapy.Field()
    product_name        = scrapy.Field()
    product_category    = scrapy.Field()
    product_description = scrapy.Field()
    product_price       = scrapy.Field()
    prodcut_images      = scrapy.Field()

class Quote(scrapy.Item):
    product_name = scrapy.Field()
