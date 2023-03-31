import scrapy

class Product(scrapy.Item):
    restaurant_name     = scrapy.Field()
    source              = scrapy.Field()
    product_name        = scrapy.Field()
    product_category    = scrapy.Field()
    product_description = scrapy.Field()
    product_price       = scrapy.Field()
    product_images      = scrapy.Field()

