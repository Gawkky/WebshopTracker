# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ReturnItem(scrapy.Item):
    name = scrapy.Field()
    original_price = scrapy.Field()
    new_price = scrapy.Field()
    url = scrapy.Field()
    score = scrapy.Field()
    cat = scrapy.Field()
    Factory_code = scrapy.Field()
    date = scrapy.Field()
    website = scrapy.Field()
    pass