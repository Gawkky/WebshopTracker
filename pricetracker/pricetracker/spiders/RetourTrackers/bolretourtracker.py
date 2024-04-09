import scrapy
from pricetracker.items import ReturnItem
from datetime import datetime


class BolretourdealtrackerSpider(scrapy.Spider):
    name = "bolretourdealtracker"
    custom_settings = {
        'ITEM_PIPELINES': {
            "pricetracker.pipelines.PricetrackerPipeline": 250,
            "pricetracker.pipelines.DuplicateItemPipeline": 350,
            "pricetracker.pipelines.SavingToMySQLPipelineBolRetour": 600,
        }
    }
    allowed_domains = ["www.bol.com"]
    start_urls = [
        "https://www.bol.com/be/nl/w/bol-com-retourdeals/1273754"]

    def parse(self, response):
        items = response.css('li.product-item--row.js_item_root')
        categories = ["+7097", "+7111", "/4294862300", "+18100/4294937500/"]
        base_url = "https://www.bol.com"
        start_url = f"{base_url}/be/nl/w/bol-com-retourdeals/1273754"
        pass

# Setting up and scraping different categories
        for category in categories:
            yield response.follow(start_url + category)
        # Setting up and scraping different items
            try:
                for item in items:
                    try:
                        next_item = item.css(
                            'a.product-title.px_list_page_product_click.list_page_product_tracking_target::attr(href)').get()
                        yield response.follow(next_item, callback=self.parse_item_page)
                    except:
                        continue
        # Making sure I get to the next page
                next_page = response.css(
                    'li.pagination__controls--next a ::attr(href)').get()

                if next_page is not None and "alle-artikelen" not in next_page:
                    next_page_url = base_url + next_page
                    yield response.follow(next_page_url, callback=self.parse)
            except:
                continue

    def parse_item_page(self, response):
        RetourDeals_Item = ReturnItem()
        item_info = response.css('div.product_page_two-column')

        RetourDeals_Item['name'] = item_info.css('h1.page-heading span::text').get()
        RetourDeals_Item['original_price'] = item_info.css('del.h-nowrap.buy-block__list-price::text').get(default='')
        new_price = item_info.css('span.promo-price::text').get(default='NULL').replace('\n', "").strip()
        fraction = item_info.css('sup.promo-price__fraction::text').get(default='').replace('\n ', "").strip()
        if new_price.endswith('.-'):
            new_price = new_price.replace('.-', '.00')
        elif fraction:
            new_price + "." + fraction
        RetourDeals_Item['new_price'] = new_price
        RetourDeals_Item['url'] = item_info.css('div.pdp-header__meta-item a wsp-share').attrib['share-url']
        RetourDeals_Item['score'] = item_info.css('div.star-rating span span.is-hidden span::text').get()
        RetourDeals_Item['cat'] = item_info.xpath("//ul[1]/li[last()]/span[1]/a[1]/p[1]/text()").get()
        Factory_code = item_info.xpath("//dt[normalize-space()='MPN (Manufacturer Part Number)']/following::dd/text()").get()
        if Factory_code:
            RetourDeals_Item['Factory_code'] = Factory_code
        else:
            RetourDeals_Item['Factory_code'] = None
        RetourDeals_Item['date'] = datetime.now().strftime('%Y%m%d')
        yield RetourDeals_Item
        pass
