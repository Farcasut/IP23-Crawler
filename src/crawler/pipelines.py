# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from crawler.items import Product
import json

items = []

class CrawlerPipeline:
    def __init__(self):
        pass

    def process_item(self, item, spider):
        global items
        new_item = ItemAdapter(item)
        return item 
