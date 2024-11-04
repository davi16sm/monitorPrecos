import scrapy
from datetime import datetime
import pytz 


class MercadoLivreSmartphoneAppleSpider(scrapy.Spider):
    name = "mercado_livre_smartphone_apple"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/celulares-telefones/celulares-smartphones/iphone/novo/_NoIndex_True?original_category_landing=true"]

    pagina = 1
    max_paginas = 10


    def parse(self, response):        
        #Obtém os "conteiners" na qual são exibidos os produtos
        produtos = response.css('div.ui-search-result__wrapper') 

        #Percorre a lista de produtos
        for produto in produtos:
            preco_fracao = ','+produto.css('div.ui-search-price__second-line').css('span.andes-money-amount__cents.andes-money-amount__cents--superscript-24::text').get() if produto.css('div.ui-search-price__second-line').css('span.andes-money-amount__cents.andes-money-amount__cents--superscript-24::text').get() != None else str(',00')

            # Obtém os retornos da chamada
            yield {
                'marca' : 'Apple', 
                'titulo' : produto.css('a.ui-search-link__title-card.ui-search-link::text').get(),
                'preco' : produto.css('div.ui-search-price__second-line').css('span.andes-money-amount__fraction::text').get() #Parte Inteira do Valor 
                'condicao': 'Novo',# Já contém um filtro no link de pesquisa da página do ecommerce
                'data_captura' : datetime.now(pytz.utc).astimezone(pytz.timezone('America/Fortaleza')).strftime("%d/%m/%Y %H:%M:%S")
            }

        # Controle da quantidade de páginas acessadas no portal. Necessário para não ser bloqueado pelo portal.
        if self.pagina < self.max_paginas:
            prox_pagina = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if prox_pagina:
                self.pagina += 1
                yield scrapy.Request(url=prox_pagina, callback=self.parse)
