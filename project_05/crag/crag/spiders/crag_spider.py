import scrapy
from crag.items import CragItem
from bs4 import BeautifulSoup as bs

class CragSpider(scrapy.Spider):
    name = "craglist_rv"
    allowed_domains = ['craigslist.org']

    def start_requests(self):
        cities = ['newyork', 'losangeles', 'chicago', 'houston', 'philadelphia',
       'phoenix', 'sanantonio', 'sandiego', 'dallas', 'sfbay',
       'austin', 'jacksonville', 'indianapolis', 'columbus',
       'fortworth', 'charlotte', 'detroit', 'elpaso', 'seattle',
       'denver', 'washington', 'memphis', 'boston', 'nashville',
       'baltimore', 'oklahomacity', 'portland', 'lasvegas',
       'louisville', 'milwaukee', 'albuquerque', 'tucson', 'fresno',
       'sacramento', 'longbeach', 'kansascity', 'mesa', 'atlanta',
       'virginiabeach', 'omaha', 'coloradosprings', 'raleigh',
       'miami', 'oakland', 'minneapolis', 'tulsa', 'cleveland',
       'wichita', 'neworleans']
        for domain in cities:
            url = 'http://%s.craigslist.org/search/sss?query=rv' %domain
            yield scrapy.Request(url, self.parse_city)


    def parse_city(self, response):
        prices = response.xpath("//span/span[@class='price']/text()").extract()
        city = response.xpath("//select/option/text()").extract_first()

        for price in prices:
          item = CragItem()
          item['rv_price'] = price
          item['rv_city'] = city
          yield item

        next_page_url = response.xpath('//a[contains(@class, "button next")]/@href').extract_first()
        abs_next_page_url = response.urljoin(next_page_url)
        request = scrapy.Request(abs_next_page_url, callback=self.parse_city)
        yield request