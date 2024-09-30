import scrapy


class AmazontweedekanstrackerSpider(scrapy.Spider):
    name = "amazontweedekanstracker"
    allowed_domains = ["amazon.com.be"]
    start_urls = ["https://amazon.com.be"]

    def parse(self, response):
        pass
