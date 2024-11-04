import scrapy


class CasasbahiaSmartphoneAppleSpider(scrapy.Spider):
    name = "casasbahia_smartphone_apple"
    allowed_domains = ["www.casasbahia.com.br"]
    start_urls = ["https://www.casasbahia.com.br/c/telefones-e-celulares/smartphones/iphone?&filtro=categoria^d:c38_c326_c3267&&utm_campaign=1735779&&utm_medium=afiliados&&utm_source=zanox&"]

    pagina = 1
    max_paginas = 10


    def parse(self, response):
        produtos = response.css('div[data-cy=divGridProducts]').css('div.css-1enexmx')
        #fuso_horario = pytz.timezone('America/Fortaleza')

        for produto in produtos:
            preco_fracao = ','+produto.css('div[data-cy=divGridProducts]').css('span.andes-money-amount__cents.andes-money-amount__cents--superscript-24::text').get() if produto.css('div.ui-search-price__second-line').css('span.andes-money-amount__cents.andes-money-amount__cents--superscript-24::text').get() != None else str(',00')


            yield {
                'marca' : 'Apple', #produto.css('span.poly-component__brand::text').get(),
                'titulo' : produto.css('h3.product-card__title span::text').get(),  
                'preco' :  produto.css('div.product-card__highlight-price::text').get(),
                'data_captura' : datetime.now(pytz.utc).astimezone(pytz.timezone('America/Fortaleza')).strftime("%d/%m/%Y %H:%M:%S")
            }

        if self.pagina < self.max_paginas:
            prox_pagina = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if prox_pagina:
                self.pagina += 1
                yield scrapy.Request(url=prox_pagina, callback=self.parse)
