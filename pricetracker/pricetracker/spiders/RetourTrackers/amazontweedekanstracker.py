import scrapy


class AmazontweedekanstrackerSpider(scrapy.Spider):
    name = "amazontweedekanstracker"
    custom_settings = {
        'ITEM_PIPELINES': {
            "pricetracker.pipelines.PriceTrackerPipeline": 250,
            "pricetracker.pipelines.DuplicateItemPipeline": 350,
            "pricetracker.pipelines.SavingToMySQLPipelineRetour": 600,
        }
    }
    allowed_domains = ["amazon.com.be"]
    start_urls = ["https://www.amazon.com.be/s?i=specialty-aps&srs=95013397031"]

    def parse(self, response):
        items = response.css('div.s-main-slot.s-result-list.s-search-results.sg-row')
        categories = ["&rh=n%3A95013397031%2Cn%3A27156257031"]
        base_url = "https://www.amazon.com.be"
        start_url = f"{base_url}/s?i=specialty-aps&srs=95013397031"
        pass

        for category in categories:
            yield response.follow(start_url + category)
            
