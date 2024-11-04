import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from scrapy.selector import Selector
from datetime import datetime
import pytz
import time

class MagazineluizaSmartphoneAppleSpider(scrapy.Spider):
    name = "magazineluiza_smartphone_apple"
    allowed_domains = ["www.magazineluiza.com.br"]
        
    # URL base sem paginação
    base_url = "https://www.magazineluiza.com.br/iphone/celulares-e-smartphones/s/te/teip/"
    total_pages = 8  # Total de páginas a serem visitadas

    def __init__(self, *args, **kwargs):
        super(MagazineluizaSmartphoneAppleSpider, self).__init__(*args, **kwargs)
        
        # Configura o WebDriver do Selenium
        options = Options()
        options.add_argument('--headless')  # Executar o Firefox em modo headless
        service = Service('/home/bigdata/IGTI/pos_engenharia_dados/projeto_aplicado/src/libs/geckodriver')
        options.log.level = "trace"
        self.driver = webdriver.Firefox(service=service, options=options)

    def start_requests(self):
        # Loop através do número de páginas que você deseja visitar
        for page in range(1, self.total_pages + 1):
            if page == 1:
                page_url = self.base_url  # Primeira página sem parâmetro
            else:
                page_url = f"{self.base_url}?page={page}"  # Adiciona o parâmetro de página a partir da segunda página

            self.driver.get(page_url)
            self.logger.info(f"Carregando a URL da página {page}")
            
            # Aguarda o carregamento da página
            time.sleep(5)  # Ajuste o tempo conforme necessário

            # Captura a página atual
            html = self.driver.page_source
            
            # Envia a requisição para a função parse
            yield scrapy.Request(url=page_url, headers=self.get_custom_headers(), callback=self.parse, meta={'html': html})

    def parse(self, response):
        html = response.meta['html']  # Obtém o HTML da meta
        selector = Selector(text=html)
        produtos = selector.css('li.sc-fTyFcS.iTkWie')

        for produto in produtos:            
            titulo = produto.css('h2[data-testid=product-title]::text').get()
            yield {
                'marca': 'Apple',  #produto.css('span.poly-component__brand::text').get(),
                'titulo': titulo,
                'preco': produto.css('p[data-testid=price-value]::text').get(),
                'condicao': 'Usado' if titulo and "usado" in titulo.lower() else 'Novo',
                'data_captura': datetime.now(pytz.utc).astimezone(pytz.timezone('America/Fortaleza')).strftime("%d/%m/%Y %H:%M:%S")
            }

    def close(self, reason):
        self.driver.quit()  # Fecha o navegador ao final
        self.logger.info("Navegador fechado.")

    def get_custom_headers(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
            'Accept-Language': 'pt-BR,pt;q=0.9',
            'Referer': 'https://www.magazineluiza.com.br/'
        }
