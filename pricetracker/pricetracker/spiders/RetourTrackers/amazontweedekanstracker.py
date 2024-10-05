import scrapy
from pricetracker.items import ReturnItem
from datetime import datetime


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
    start_urls = ["https://www.amazon.com.be/"]

    def parse(self, response):
        items = response.css('div.sg-col-20-of-24.s-result-item.s-asin.sg-col-0-of-12.sg-col-16-of-20.sg-col.s-widget-spacing-small.sg-col-12-of-16')
        categories = ["s?i=electronics"]
        base_url = "https://www.amazon.com.be"
        language = "&language=nl_BE"
        start_url = f"{base_url}/"
        pass

        for category in categories:
            yield response.follow(start_url + category + '&srs=95013409031' + language)

            try:
                for item in items:
                    try:
                        next_item = item.css('a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal::attr(href)').get()
                        yield response.follow(next_item, callback=self.parse_item_page)
                    except:
                        continue
                next_page = response.css('a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator::attr(href)').get()

                if next_page is not None:
                    next_page_url = base_url + next_page
                    yield response.follow(next_page_url, callback=self.parse)
            except:
                continue
    
    def parse_item_page(self, response):
        Tweedekans_Item = ReturnItem()
        item_info = response.css('div.centerColAlign')

        Tweedekans_Item['name'] = item_info.css('span.a-size-large.product-title-word-break::text').get()
        Tweedekans_Item['original_price'] = item_info.css('span.basisPrice span span.a-offscreen::text').get(default='')
        new_price = item_info.css('span.a-price-whole::text').get(default='NULL')
        fraction = item_info.css('span.a-price-fraction::text').get(default='')
        new_price + "." + fraction
        Tweedekans_Item['new_price'] = new_price
        Tweedekans_Item['url'] = response.request.url
        Tweedekans_Item['score'] = item_info.css('span.reviewCountTextLinkedHistogram.noUnderline span a span::text').get()
        Tweedekans_Item['score'] = response.xpath("//div[contains(@id, 'showing-breadcrumbs_div')]/div/div/div/ul/li[last()]/span/a/text()").get()
        Tweedekans_Item['cat'] = response.xpath("//div[@id='nav-subnav']/@data-category").get()
        Tweedekans_Item['Factory_code'] = item_info.xpath("//div[contains(@id, 'title_feature_div')]/@data-csa-c-asin").get()
        Tweedekans_Item['date'] = datetime.now().strftime('%Y%m%d')
        Tweedekans_Item['website'] = 'amazon'
        yield Tweedekans_Item
        pass