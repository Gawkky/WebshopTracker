import scrapy
from pricetracker.items import CompareItem
from datetime import datetime
from pricetracker.middlewares import DatabaseMiddleware

class BolSpider(scrapy.Spider):
    name = "bol"
    custom_settings = {
        'ITEM_PIPELINES': {
            "pricetracker.pipelines.priceComparerPipeline": 100,
            "pricetracker.pipelines.DuplicateItemPipeline": 350,
            "pricetracker.pipelines.SavingToMySQLPipelineComparer": 400,
        }
    }
    allowed_domains = ["bol.com"]
    start_urls = ["https://www.bol.com"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.middleware = DatabaseMiddleware()  # Initialize the middleware
        self.middleware.assign_product_names(self)  # Assign product names to the spider


    def parse(self, response):
        search_url = f"{self.start_urls[0]}/be/nl/s/?searchtext="
        product_names = self.product_names 
        pass

        for item in product_names:
            item_query = item.replace(" ", "%20")
            yield response.follow(search_url + item_query, callback=self.item_parse, cb_kwargs={'item': item, 'url': self.start_urls[0]})
            
    def item_parse(self, response, item, url):   
        Product = CompareItem()
        item_info = response.css("div.results-area")

        Product['site'] = self.name
        Product['name'] = item
        Product['price'] = item_info.xpath("//meta[@itemprop='price']/@content").get()
        if Product['price'] != None:
            Product['url'] = url + item_info.css('a.product-title.px_list_page_product_click.list_page_product_tracking_target::attr(href)').get()
        Product['date'] = datetime.now().strftime('%Y%m%d')
        yield Product
        pass