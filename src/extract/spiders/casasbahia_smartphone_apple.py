import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
from datetime import datetime
import pytz
import time

class CasasbahiaSmartphoneAppleSpider(scrapy.Spider):
    name = "casasbahia_smartphone_apple"
    allowed_domains = ["www.casasbahia.com.br"]
    
    # URL base sem paginação
    base_url = "https://www.casasbahia.com.br/c/telefones-e-celulares/smartphones/iphone?&&filtro=categoria^d:c38_c326_c3267&&utm_campaign=1735779&&utm_medium=afiliados&&utm_source=zanox&"
    total_pages = 14  # Total de páginas a serem visitadas

    def __init__(self, *args, **kwargs):
        super(CasasbahiaSmartphoneAppleSpider, self).__init__(*args, **kwargs)
        
        # Configura o WebDriver do Selenium
        options = Options()
        options.add_argument('--headless')  # Executar o Firefox em modo headless
        service = Service('/home/bigdata/IGTI/pos_engenharia_dados/projeto_aplicado/src/libs/geckodriver')
        options.log.level = "trace"
        self.driver = webdriver.Firefox(service=service, options=options)

    def start_requests(self):
          # Acessa a URL inicial
        self.driver.get(self.base_url)
        self.logger.info("Carregando a URL inicial")
        
        # Captura os cookies após carregar a página inicial
        cookies = self.driver.get_cookies()  # Captura os cookies
        for cookie in cookies:
            self.driver.add_cookie(cookie)  # Adiciona cookies ao navegador

        # Captura a primeira página (sem número)
        html = self.driver.page_source
        yield scrapy.Request(url=self.base_url,headers=self.get_custom_headers(), callback=self.parse, meta={'html': html})


    def parse(self, response):
        html = response.meta['html']  # Obtém o HTML da meta
        selector = Selector(text=html)
        produtos = selector.css('div[data-cy=divGridProducts] div.css-1enexmx')

        for produto in produtos:
            # Retorna um dicionário como item
            yield {
                'marca': 'Apple',
                'titulo': produto.css('h3.product-card__title span::text').get(),
                'preco': produto.css('div.product-card__highlight-price::text').get(),
                'data_captura': datetime.now(pytz.utc).astimezone(pytz.timezone('America/Fortaleza')).strftime("%d/%m/%Y %H:%M:%S")
            }

    def close(self, reason):
        self.driver.quit()  # Fecha o navegador ao final
        self.logger.info("Navegador fechado.")


    def get_custom_headers(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
            'Accept-Language': 'pt-BR,pt;q=0.9',
            'Referer': 'https://www.casasbahia.com.br/'
        }