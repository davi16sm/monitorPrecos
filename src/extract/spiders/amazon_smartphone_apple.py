import scrapy
from datetime import datetime
import pytz 


class AmazonSmartphoneAppleSpider(scrapy.Spider):
    name = "amazon_smartphone_apple"
    allowed_domains = ["www.amazon.com.br"]
    start_urls = ["https://www.amazon.com.br/s?k=apple&rh=n%3A16209062011%2Cn%3A16243890011&dc&ds=v1%3AJYLnTzH7lS98pNscbRnGqEelWlyT4qrqJCA9S9pqCQQ&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=39O10XWONVPNO&qid=1728936322&rnid=18726358011&sprefix=apple%2Caps%2C253&ref=sr_nr_n_2"]
           
    pagina = 1
    max_paginas = 10


    def parse(self, response):
        produtos = response.css('div[data-component-type=s-search-result]')
        #fuso_horario = pytz.timezone('America/Fortaleza')

        for produto in produtos:
            preco_fracao = ','+produto.css('div.ui-search-price__second-line').css('span.andes-money-amount__cents.andes-money-amount__cents--superscript-24::text').get() if produto.css('div.ui-search-price__second-line').css('span.andes-money-amount__cents.andes-money-amount__cents--superscript-24::text').get() != None else str(',00')


            yield {
                'marca' : 'Apple', #produto.css('span.poly-component__brand::text').get(),
                'titulo' : produtos.css('div[data-cy=title-recipe]').css('a span::text').get(),  
                'preco' :  produtos.css('div[data-cy=price-recipee]').css('a span.a-price::text').get(),
                'data_captura' : datetime.now(pytz.utc).astimezone(pytz.timezone('America/Fortaleza')).strftime("%d/%m/%Y %H:%M:%S")
            }

        if self.pagina < self.max_paginas:
            prox_pagina = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if prox_pagina:
                self.pagina += 1
                yield scrapy.Request(url=prox_pagina, callback=self.parse)
