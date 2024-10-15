import scrapy


class MagazineluizaSmartphoneSamsungSpider(scrapy.Spider):
    name = "magazineluiza_smartphone_samsung"
    allowed_domains = ["www.magazineluiza.com.br"]
    start_urls = ["https://www.magazineluiza.com.br/smartphone/celulares-e-smartphones/s/te/tcsp/brand---samsung/"]

    def parse(self, response):
        pass
