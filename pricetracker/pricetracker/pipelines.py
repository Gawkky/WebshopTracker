# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
from scrapy.utils.url import canonicalize_url
from scrapy.exceptions import DropItem
import mysql.connector
import re
from dotenv import load_dotenv
import os

load_dotenv()

class PricetrackerPipeline:
    def process_item(self, item, spider):
        item['name'] = item['name'].replace('\n', '').strip().replace("Tweedekans ", "")
        item['original_price'] = item['original_price'].replace('\n', '').replace(".", "").replace(",", ".").replace('.-', '.00').strip()
        if item['original_price']:
            item['original_price'] = float(item['original_price'])
        else:
            item['original_price'] = None
        item['url'] = item['url'].replace('?referrer=socialshare_pdp_www', '')
        item['score'] = float(item['score'].replace(",", ".")) if item['score'] else '0.00'
        item['cat'] = item['cat'].replace('\n', '').strip()
        if item['Factory_code'] != None:
            item['Factory_code'] = item['Factory_code'].replace('\n', '').strip()
        return item

class priceComparerPipeline:
    def process_item(self, item, spider):
        item['name'] = item['name'].replace('\n', '').strip()
        if item['price'] == None:
            item['price'] = "Null"
            item['url'] = "Null"
        else:
            item['price'] = item['price'].replace(",",".").replace(".-",".00").replace("\xa0€", "").replace("\u202f", "")
            item['url'] = re.sub(r'/ref=.*', '', item['url'])
        return item

class DuplicateItemPipeline(object):
    def __init__(self):
        self.seen_urls = set()

    def process_item(self, item, spider):
        item_url = canonicalize_url(item['url'])
        len_url = len(item_url)
        if len_url > 255:
            raise DropItem(f"URL is too long, product probably incorrect: {item['name']}")
        if item_url in self.seen_urls:
            raise DropItem(f'Duplicate item found: {item_url}')
        else:
            self.seen_urls.add(item_url)
            return item


class SavingToMySQLPipelineBolRetour(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE'),
            port=os.getenv('DB_PORT')
        )
        self.curr = self.connection.cursor()

    def create_table(self):
        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS bol_com (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                original_price FLOAT,
                new_price FLOAT,
                url VARCHAR(255),
                score FLOAT,
                cat VARCHAR(50),
                Factory_code VARCHAR(255),
                date DATE
            )
        """)
        self.connection.commit()

    def process_item(self, item, spider):
        self.create_table()

        if self.is_item_exists(item):
            return item

        self.store_db(item)
        return item

    def is_item_exists(self, item):
        # Implement your logic to check if the item already exists in the database
        query = "SELECT COUNT(*) FROM bol_com WHERE name = %s AND original_price = %s AND new_price = %s AND url = %s AND score = %s AND cat = %s AND Factory_code =%s AND date = %s"

        self.curr.execute(query, (item['name'], item['original_price'],
                          item['new_price'], item['url'], item['score'], item['cat'], item['Factory_code'], item['date']))
        result = self.curr.fetchone()

        return result[0] > 0

    def store_db(self, item):
        self.curr.execute(
            "INSERT INTO bol_com (name, original_price, new_price, url, score, cat, Factory_code, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (item['name'], item['original_price'], item['new_price'],
             item['url'], item['score'], item['cat'], item['Factory_code'], item['date'])
        )
        self.connection.commit()

    def close_spider(self, spider):
        self.curr.close()
        self.connection.close()

class SavingToMySQLPipelineCoolblueRetour(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE'),
            port=os.getenv('DB_PORT')
        )
        self.curr = self.connection.cursor()

    def create_table(self):
        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS coolblue (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                original_price FLOAT,
                new_price FLOAT,
                url VARCHAR(255),
                score FLOAT,
                Factory_code VARCHAR(255),
                cat VARCHAR(50),
                date DATE
            )
        """)
        self.connection.commit()

    def process_item(self, item, spider):
        self.create_table()

        if self.is_item_exists(item):
            return item

        self.store_db(item)
        return item

    def is_item_exists(self, item):
        # Implement your logic to check if the item already exists in the database
        query = "SELECT COUNT(*) FROM coolblue WHERE name = %s AND original_price = %s AND new_price = %s AND url = %s AND score = %s AND cat = %s AND factory_code = %s AND date = %s"

        self.curr.execute(query, (item['name'], item['original_price'],
                          item['new_price'], item['url'], item['score'], item['cat'], item['Factory_code'], item['date']))
        result = self.curr.fetchone()

        return result[0] > 0

    def store_db(self, item):
        self.curr.execute(
            "INSERT INTO coolblue (name, original_price, new_price, url, score, cat, Factory_code, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (item['name'], item['original_price'], item['new_price'],
             item['url'], item['score'], item['cat'], item['Factory_code'], item['date'])
        )
        self.connection.commit()

    def close_spider(self, spider):
        self.curr.close()
        self.connection.close()

class SavingToMySQLPipelineComparer(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE'),
            port=os.getenv('DB_PORT')
        )
        self.curr = self.connection.cursor()

    def create_table(self):
        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS priceComparer (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                price VARCHAR(255),
                site VARCHAR(255),
                url VARCHAR(255),
                date DATE
            )
        """)
        self.connection.commit()

    def process_item(self, item, spider):
        self.create_table()

        if self.is_item_exists(item):
            return item

        self.store_db(item)
        return item

    def is_item_exists(self, item):
        try:
            # Implement your logic to check if the item already exists in the database
            query = "SELECT COUNT(*) FROM priceComparer WHERE name = %s AND price = %s AND site = %s AND url = %s AND date = %s"

            self.curr.execute(query, (item['name'], item['price'], item['site'], item['url'], item['date']))
            result = self.curr.fetchone()
            return result[0] > 0
        except mysql.connector.Error as err:
            print("Error:", err)
            return False

    def store_db(self, item):
        self.curr.execute(
            "INSERT INTO priceComparer (name, price, site, url, date) VALUES (%s, %s, %s, %s, %s)",
            (item['name'], item['price'], item['site'], item['url'], item['date'])
        )
        self.connection.commit()

    def close_spider(self, spider):
        self.curr.close()
        self.connection.close()