import scrapy
from pricetracker.items import CompareItem
from datetime import datetime
from pricetracker.middlewares import DatabaseMiddleware
import re


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    custom_settings = {
        'ITEM_PIPELINES': {
            "pricetracker.pipelines.priceComparerPipeline": 100,
            "pricetracker.pipelines.DuplicateItemPipeline": 350,
            "pricetracker.pipelines.SavingToMySQLPipelineComparer": 400,
        }
    }
    allowed_domains = ["amazon.com.be"]
    start_urls = ["https://amazon.com.be"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.middleware = DatabaseMiddleware()  # Initialize the middleware
        self.middleware.assign_product_names(self)  # Assign product names to the spider

    def parse(self, response):
        search_url = f"{self.start_urls[0]}/s?k="
        product_names = self.product_names
        pass

        for item in product_names:
            item_query = item.replace(" ", "+")
            yield response.follow(search_url + item_query, callback=self.item_parse, cb_kwargs={'item': item, 'url': self.start_urls[0]})

    def item_parse(self, response, item, url):   
        Product = CompareItem()

        Product['site'] = self.name
        Product['name'] = item
        Product['price'] = response.xpath("//span[@class='a-offscreen']/text()").get()
        if Product['price'] != None:
            Product['url'] = url + response.xpath("//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']/@href").get()
        Product['date'] = datetime.now().strftime('%Y%m%d')
        yield Product
        pass