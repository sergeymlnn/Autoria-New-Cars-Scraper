from scrapy import Spider as ScrapySpider
from scrapy.shell import inspect_response
from scrapy.crawler import CrawlerProcess
from scrapy.http.response.html import HtmlResponse


# python spider.py or scrapy runspider spider.py -o cars.json
class Spider(ScrapySpider):
  """Spider to collect available car brands and their number on the market"""
  name = "auto_ria_spider"
  allowed_domains = "auto.ria.com"
  start_urls = ["https://auto.ria.com/uk/newauto/catalog/"]
  custom_settings = {
    "COOKIES_ENABLED": False,
    "DOWNLOAD_DELAY": 2,
    "ROBOTSTXT_OBEY": False,
    "LOG_LEVEL": "INFO",
  }


  def parse(self, response: HtmlResponse) -> None:
    """Extracts car brands and their number on the market"""
    # inspect_response(response, self)
    items = response.xpath("//a[@class='item-brands']/span[@class='top-brand']")
    for item in items:
      brand = item.xpath(".//span[@class='name']/text()").get()
      quantity = item.xpath(".//span[@class='count']/text()").get("").strip("()")
      yield {
        "brand": brand,
        "quantity": quantity,
      }


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(Spider)
    process.start()
    