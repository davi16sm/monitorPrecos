import scrapy
from datetime import datetime
import pytz 


class MagazineluizaSmartphoneAppleSpider(scrapy.Spider):
    name = "magazineluiza_smartphone_apple"
    allowed_domains = ["www.magazineluiza.com.br"]
    start_urls = ["https://www.magazineluiza.com.br/iphone/celulares-e-smartphones/s/te/teip/"]

    pagina = 1
    max_paginas = 10


    def parse(self, response):
        produtos = response.css('li.sc-fTyFcS.iTkWie')
        #fuso_horario = pytz.timezone('America/Fortaleza')

        for produto in produtos:
            preco_fracao = ','+produto.css('div.ui-search-price__second-line').css('span.andes-money-amount__cents.andes-money-amount__cents--superscript-24::text').get() if produto.css('div.ui-search-price__second-line').css('span.andes-money-amount__cents.andes-money-amount__cents--superscript-24::text').get() != None else str(',00')


            yield {
                'marca' : 'Apple', #produto.css('span.poly-component__brand::text').get(),
                'titulo' : produto.css('h2[data-testid=product-title]::text').get(),  
                'preco' :  produto.css('p[data-testid=price-value]::text').get(),
                'data_captura' : datetime.now(pytz.utc).astimezone(pytz.timezone('America/Fortaleza')).strftime("%d/%m/%Y %H:%M:%S")
            }

        if self.pagina < self.max_paginas:
            prox_pagina = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if prox_pagina:
                self.pagina += 1
                yield scrapy.Request(url=prox_pagina, callback=self.parse)
