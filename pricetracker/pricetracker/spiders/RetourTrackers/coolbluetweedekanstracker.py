import scrapy
from pricetracker.items import ReturnItem
from datetime import datetime


class CoolbluetweedekanstrackerSpider(scrapy.Spider):
    name = "coolbluetweedekanstracker"
    custom_settings = {
        'ITEM_PIPELINES': {
            "pricetracker.pipelines.PriceTrackerPipeline": 250,
            "pricetracker.pipelines.DuplicateItemPipeline": 350,
            "pricetracker.pipelines.SavingToMySQLPipelineRetour": 600,
        }
    }
    allowed_domains = ["coolblue.be"]
    start_urls = ["https://www.coolblue.be/nl/tweedekans/filter"]

    def parse(self, response):
        items = response.css('div.product-card__title')
        categories = ["/producttype:routers", "/producttype:solid-state-drives-ssd", "/producttype:interne-harde-schijven", "/producttype:geheugenkaarten", "/merk:apple", "/producttype:televisies/merk:samsung"]
        base_url = "https://www.coolblue.be"
        start_url = f"{base_url}/nl/tweedekans/filter"
        pass
    
        for category in categories:
            yield response.follow(start_url + category)
        # Setting up and scraping different items
            try:
                for item in items:
                    try:
                        next_item = item.css(
                            'div.product-card__title div a.link::attr(href)').get()
                        yield response.follow(next_item, callback=self.parse_item_page)
                    except:
                        continue
        # Making sure I get to the next page
                next_page = response.css(
                    'li.pagination__item.pagination__item--arrow>a.pagination__link ::attr(href)').get()
                
                if next_page is not None:
                    next_page_url = start_url + next_page
                    yield response.follow(next_page_url, callback=self.parse)
            except:
                continue

    def parse_item_page(self,response):
        Tweedekans_Item = ReturnItem()
        item_info = response.css('div.pt--3\@sm.js-layout-content')

        Tweedekans_Item['name'] = item_info.css('h1.js-product-name::text').get()
        Tweedekans_Item['original_price'] = item_info.css('span.sales-price__former-price::text').get(default='')
        Tweedekans_Item['new_price'] = item_info.css('strong.sales-price__current.js-sales-price-current::text').get(default='NULL').replace('\n', '').strip().replace(".", "").replace(",", ".").replace('.-', '.00')
        Tweedekans_Item['url'] = response.request.url
        # Built scores
        score = item_info.css('span.review-rating__reviews.text--truncate::text').get().replace('\n', '').strip().split('/',1)[0].replace(".", "").replace(",", ".").replace('.-', '.00')
        if score != "0 reviews":
            Tweedekans_Item['score'] = score
        else:
            Tweedekans_Item['score'] = None
        Tweedekans_Item['cat'] = item_info.xpath('//ol[1]/li[1]/a[1]/text()').get()
        Tweedekans_Item['Factory_code'] = item_info.xpath("//dl[@data-property-name='Fabrikantcode']/dd/text()").get()
        Tweedekans_Item['date'] = datetime.now().strftime('%Y%m%d')
        Tweedekans_Item['website'] = 'coolblue'
        yield Tweedekans_Item
        pass