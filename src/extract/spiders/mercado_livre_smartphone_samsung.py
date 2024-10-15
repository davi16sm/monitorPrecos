import scrapy
from datetime import datetime
import pytz 


class MercadoLivreSmartphoneSamsungSpider(scrapy.Spider):
    name = "mercado_livre_smartphone_samsung"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/celulares-telefones/celulares-smartphones/samsung/novo/_Loja_all#applied_filter_id%3Dofficial_store%26applied_filter_name%3DLojas+oficiais%26applied_filter_order%3D8%26applied_value_id%3Dall%26applied_value_name%3DSomente+lojas+oficiais%26applied_value_order%3D1%26applied_value_results%3D148%26is_custom%3Dfalse"]

    pagina = 1
    max_paginas = 10


    def parse(self, response):        
        produtos = response.css('div.ui-search-result__wrapper')
        #fuso_horario = pytz.timezone('America/Fortaleza')

        for produto in produtos:
            preco_fracao = ','+produto.css('div.ui-search-price__second-line').css('span.andes-money-amount__cents.andes-money-amount__cents--superscript-24::text').get() if produto.css('div.ui-search-price__second-line').css('span.andes-money-amount__cents.andes-money-amount__cents--superscript-24::text').get() != None else str(',00')


            yield {
                'marca' : 'Samsung', #produto.css('span.poly-component__brand::text').get(),
                'titulo' : produto.css('a.ui-search-link__title-card.ui-search-link::text').get(),
                'preco' : produto.css('div.ui-search-price__second-line').css('span.andes-money-amount__fraction::text').get() #Parte Inteira do Valor
                          + preco_fracao,  #Parte Fração do Valor                        
                'data_captura' : datetime.now(pytz.utc).astimezone(pytz.timezone('America/Fortaleza')).strftime("%d/%m/%Y %H:%M:%S")
            }

        if self.pagina < self.max_paginas:
            prox_pagina = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if prox_pagina:
                self.pagina += 1
                yield scrapy.Request(url=prox_pagina, callback=self.parse)
