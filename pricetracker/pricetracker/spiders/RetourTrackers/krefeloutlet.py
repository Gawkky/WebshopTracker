import scrapy
from pricetracker.items import ReturnItem
from datetime import datetime


class KrefeloutletSpider(scrapy.Spider):
    name = "krefeloutlet"
    custom_settings = {
        'ITEM_PIPELINES': {
            "pricetracker.pipelines.PriceTrackerPipeline": 250,
            "pricetracker.pipelines.DuplicateItemPipeline": 350,
            "pricetracker.pipelines.SavingToMySQLPipelineRetour": 600,
        }
    }
    allowed_domains = ["krefel.be"]
    start_urls = ["https://www.krefel.be/nl/outlet"]

    def parse(self, response):
        items = response.response.css('div.relative.flex.flex-row.items-start.justify-center.gap-4.py-3')
        categories = ["%3Acategory%3AC738", "%3Acategory%3Aacc-15-3", "%3Acategory%3AC948", "%3Acategory%3AC881"]
        base_url = "https://www.krefel.be"
        start_url = f"{base_url}/nl/outlet?q=%3Arelevance"
        page_number = 1
        pass

        for category in categories:
            yield response.follow(start_url + category)
            try:
                for item in items:
                    try:
                        next_item = item.css('a.font-h4.font-bold.cursor-pointer.focus-border.no-underline.line-clamp-2.text-black::attr(href)').get()
                        yield response.follow(next_item, callback=self.parse_item_page)
                    except:
                        continue
                
                next_page_url = f"{base_url}/nl/outlet?currentPage={page_number}&pageSize=&q=%3Arelevance{category}"
                page_number =+ 1

                try:
                    yield response.follow(next_page_url, callback=self.parse)
                except:
                    continue
            except:
                continue

    def parse_item_page(self, response):
        Outlet_Item = ReturnItem()
        item_info = response.xpath("//div[@data-analytics-event='product-detail-impression']")

        name = item_info.css('div.ProductHeader-styled__StyledProductHeader-sc-a5fb15a5-0 div div h1::text').getall()
        Outlet_Item['name'] = ''.join(name).strip()
        Outlet_Item['original_price'] = item_info.css('div.Price-styled__StyledPriceWrapper-sc-7e79fb8-0 span span::text').get(default='')
        Outlet_Item['new_price'] = item_info.css('span.Price-styled__StyledPrice-sc-7e79fb8-1.knnIrU span::text').get(default='').replace('€\xa0', '').replace('.', '').replace(',','.').strip()
        Outlet_Item['url'] = response.request.url
        Outlet_Item['score'] = 'NULL'
        Outlet_Item['cat'] = item_info.xpath("//div[contains(@class, 'Breadcrumb-styled__StyledBreadcrumb-sc-f7c310d-0')]/div/div[2]/a[last()]/span/text()").get()
        Outlet_Item['Factory_code']= 'NULL'
        Outlet_Item['date'] = datetime.now().strftime('%Y%m%d')
        Outlet_Item['website'] = 'krefel'
        yield Outlet_Item
        pass