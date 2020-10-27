import scrapy
from ..items import WebcrawlerItem
# from webcrawler.webcrawler.items import WebcrawlerItem
from scrapy.crawler import CrawlerProcess


class NikeScraper(scrapy.Spider):
    name = "nike-scraper"
    start_urls = ["https://www.nike.com/nl/en/w/stefan-janoski-skateboarding-shoes-8mfrfz9i3pxzy7ok"]
    # The list of URLs we are going to scrape. In this case it has only one element

    # Next line creates a csv file named: auto-nike-scraped.csv when the code is executed
    custom_settings = {
        "FEED_FORMAT": "csv", "FEED_URI": "auto-nike-scraped.csv",
    }

    def parse(self, response):
        items = WebcrawlerItem()
        title = response.css("title::text").extract_first()
        items["title"] = title
        h1 = response.css("h1::text").extract()
        items["h1"] = h1
        product_info = response.css("div.product-card__body")  # Assigning product information in to product_info so
        # that we dont have to invoke "response" each time
        for product in product_info:
            shoe_name = product.css(".product-card__title::text").extract()
            shoe_kind = product.css(".product-card__subtitle::text").extract()
            shoe_price = product.css(".product-price::text").extract()

            items["shoe_kind"] = shoe_kind
            items["shoe_name"] = shoe_name
            items["shoe_price"] = shoe_price

            yield items


# running the spider
process = CrawlerProcess()
process.crawl(NikeScraper)
process.start()
