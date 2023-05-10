# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from crawler.items import Product
from urllib.parse import urlparse
from scrapy.crawler import signals 
import json
import hashlib
import psycopg2
import requests
import boto3
import os

from crawler.utils import get_rid_of_special_spaces

restaurants_hashmap = {}

class CrawlerPipeline:
    
    @classmethod
    def from_crawler(cls, crawler):
        crawler_pipeline = cls()
        crawler.signals.connect(crawler_pipeline.close_spider, signal=signals.spider_closed)
        return crawler_pipeline

    def __init__(self):
        global restaurants_hashmap
        self.filename = 'restaurants_map.json'
        if os.path.exists(self.filename):
            data = open(self.filename, 'r').read()
            restaurants_hashmap = json.loads(data)
        

    def remove_plurals(self, words):
        new_words = []
        for word in words:
            if word.endswith('es'):
                new_words.append(word[:-2])
            elif word.endswith('s'):
                new_words.append(word[:-1])
            else:
                new_words.append(word)
        return new_words 

    def generate_restaurant_key(self, argument):
        if 'Tribeca' in argument:
            return 'tribeca'
        if 'Bubble Waffle' in argument:
            return 'bubblewaffle'
        banned_words = ['restaurant', 'iasi', 'cofetăria', 'cofetaria', 'pizzeria', 'pizzerie', 'pizza', 'and', 'pacurari', 'la', 'vatra', 'delivery', 'nicolina', 'express', 'palas', 'mall', 'iulius', 'pasta', 'bar', 'stefan', 'cel', 'mare', 'costache', 'negri', 'cantemir', 'cu', 'maia', 'quisine', 'cuisine', 'timisoreana', 'bucium', 'egros', 'felicia', 'shopping', 'cafe', 'food', 'feelings', 'friends', 'drink', 'drinks', 'food', 'mexican', 'brunch', 'kiosk', 'pub', 'the', 'raw', 'vegan', 'american', 'by', 'selgros']
        argument = argument.lower() filtered_words = filter(lambda x: x not in banned_words, argument.split(' '))
        filtered_words = self.remove_plurals(filtered_words)
        return ''.join(filter(lambda x: x.isalnum(), filtered_words))

    def process_item(self, item, spider):
        global restaurants_hashmap
        item['name'] = item['name'].strip()
        if item.get('description') is not None:
            item['description'] = item['description'].strip()
        else:
            item['description'] = ''
        if item.get('category') is not None:
            item['category'] = item['category'].strip()
        else:
            item['category'] = ''
        if item.get('images') is None:
            item['images'] = []
        
        restaurant_key = self.generate_restaurant_key(item['restaurant_name'])
        if restaurant_key not in restaurants_hashmap:
            restaurants_hashmap[restaurant_key] = item['restaurant_name']
        
        item['restaurant_name'] = restaurants_hashmap[restaurant_key]
        return item
    
    def close_spider(self, spider):
        global restaurants_hashmap
        data = json.dumps(restaurants_hashmap)
        with open(self.filename, 'w') as file:
            file.write(data)

already_downloaded_images_list = []

from crawler.utils import parse_config
class DownloadImages:

    def __init__(self):
        global already_downloaded_images_list
        self.mime_to_extension = {
                    'image/jpeg': '.jpg',
                    'image/jpg': '.jpg',
                    'image/png': '.png',
                    'image/apng': '.apng',
                    'image/gif': '.gif',
                    'image/bmp': '.bmp',
                    'image/x-windows-bmp': '.bmp',
                    'image/webp': '.webp',
                    'image/svg+xml': '.svg', }
        self.headers = {
                    'Connection': 'keep-alive',
                }
        
        config_s3 = parse_config('crawler/configs/s3.ini', section='default')
        session = boto3.Session(**config_s3)
        s3 = session.resource('s3')
        bucket_name = 'crawlerphotobucket'
        self.opened_bucket = s3.Bucket(bucket_name)
        
        if len(already_downloaded_images_list) == 0:
            for i in self.opened_bucket.objects.all():
                already_downloaded_images_list.append(i.key)

    def process_item(self, item, spider):
        downloaded_images = []
        for image in item['images']:
            if self.is_valid_url(image):
                downloaded_images.append(self.download_image(spider, image))
        item['images'] = downloaded_images
        return item

    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def download_image(self, spider, image_url) -> str|None:
        global already_downloaded_images_list
        if hasattr(spider, 'requests_session') == False:
            spider.requests_session = requests.Session()
        requested = spider.requests_session.get(image_url, headers=self.headers) 

        image_data = requested.content
        try:
            file_extension = self.mime_to_extension[requested.headers['Content-Type']] 
        except KeyError:
            return None

        filename = hashlib.sha256(image_data).hexdigest()
        full_filename = filename + file_extension
        
        if full_filename in already_downloaded_images_list:
            return None

        try: 
            self.opened_bucket.put_object(Key=full_filename, Body=image_data)
            already_downloaded_images_list.append(full_filename)
        except:
            print(f"Error while trying file to upload the filename {full_filename}")
            return None

        return full_filename

from crawler.utils import create_db_connection
class PostgresPipeline:
    query_products = "INSERT INTO products(product_id, product_data) VALUES (%s, %s) ON CONFLICT (product_id) DO UPDATE SET product_data=excluded.product_data"
    query_restaurants = "INSERT INTO restaurants(restaurant_id, restaurant_data) VALUES (%s, %s) ON CONFLICT DO NOTHING"

    def open_spider(self, spider):
        self.connection = create_db_connection() 
        self.cur = self.connection.cursor()
        
    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        json_item = json.dumps(dict(item))
        json_restaurant = json.dumps({"restaurant_name": item['restaurant_name']})

        try:
            self.cur.execute('BEGIN')
            self.cur.execute(PostgresPipeline.query_restaurants, (self.generate_hash_restaurant(item), json_restaurant)) 
            self.cur.execute(PostgresPipeline.query_products, (self.generate_hash(item), json_item)) 
            self.connection.commit()
        except psycopg2.Error as e:
            print("Error inserting data: ", e, e.with_traceback)

        return item
    
    def generate_hash_restaurant(self, item):
        data = item['restaurant_name']
        data = str(data).encode('utf-8')
        return hashlib.sha1(data).hexdigest()

    def generate_hash(self, item):
        data = item['restaurant_name']+item['name']+item['source']
        data = str(data).encode('utf-8')
        return hashlib.sha1(data).hexdigest()
