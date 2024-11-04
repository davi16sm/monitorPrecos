import scrapy


class CasasbahiaSmartphoneSamsungSpider(scrapy.Spider):
    name = "casasbahia_smartphone_samsung"
    allowed_domains = ["www.casasbahia.com.br"]
    start_urls = ["https://www.casasbahia.com.br/c/telefones-e-celulares/samsung?&filtro=categoria^d:c38&filtro=marca^d:m459&&utm_source=zanox&&utm_medium=afiliados&&utm_campaign=1735779&"]

  
    pagina = 1
    max_paginas = 10


    def parse(self, response):
        produtos = response.css('li.sc-fTyFcS.iTkWie')
        #fuso_horario = pytz.timezone('America/Fortaleza')

        for produto in produtos:
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
