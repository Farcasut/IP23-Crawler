# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from crawler.items import Product
from urllib.parse import urlparse
import json
import hashlib
import psycopg2
import requests

from crawler.utils import get_rid_of_special_spaces
class CrawlerPipeline:
    def __init__(self):
        pass

    def process_item(self, item, spider):
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
        return item

class DownloadImages:
    
    @classmethod
    def from_crawler(cls, crawler):
        download_settings_path = crawler.settings.get('DOWNLOAD_IMAGES_PATH')

        if download_settings_path is not None:
            downloader = cls(download_settings_path)
        else:
            downloader = cls('images')
        return downloader

    def __init__(self, path):
        self.path = path
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
    
        try: 
            with open(self.path+'/'+full_filename, 'wb') as file:
                file.write(image_data)
        except:
            print(f"Error while trying file to write in filname {self.path}/{full_filename}")
            return None

        return full_filename

from crawler.utils import create_db_connection
class PostgresPipeline:
    query = "INSERT INTO products(product_id, product_data) VALUES (%s, %s) ON CONFLICT (product_id) DO UPDATE SET product_data=excluded.product_data"

    def open_spider(self, spider):
        self.connection = create_db_connection() 
        self.cur = self.connection.cursor()
        
    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        json_item = json.dumps(dict(item))
        self.cur.execute(PostgresPipeline.query, (self.generate_hash(item), json_item)) 
        self.connection.commit()
        return item

    def generate_hash(self, item):
        data = item['restaurant_name']+item['name']+item['source']
        data = str(data).encode('utf-8')
        return hashlib.sha1(data).hexdigest()
