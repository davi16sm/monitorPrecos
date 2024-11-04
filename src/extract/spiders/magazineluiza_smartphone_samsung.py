import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from scrapy.selector import Selector
from datetime import datetime
import pytz
import time
from selenium.webdriver.common.by import By

class MagazineluizaSmartphoneSamsungSpider(scrapy.Spider):
    name = "magazineluiza_smartphone_samsung"
    allowed_domains = ["www.magazineluiza.com.br"]
        
    # URL base sem paginação
    base_url = "https://www.magazineluiza.com.br/smartphone/celulares-e-smartphones/s/te/tcsp/brand---samsung/"
    
    def __init__(self, *args, **kwargs):
        super(MagazineluizaSmartphoneSamsungSpider, self).__init__(*args, **kwargs)
        
        # Configura o WebDriver do Selenium
        options = Options()
        options.add_argument('--headless')  # Executar o Firefox em modo headless
        service = Service('/home/bigdata/IGTI/pos_engenharia_dados/projeto_aplicado/src/libs/geckodriver')
        options.log.level = "trace"
        self.driver = webdriver.Firefox(service=service, options=options)

    def start_requests(self):
        self.driver.get(self.base_url)
        self.logger.info("Carregando a URL inicial")
        
        # Captura os cookies após carregar a página inicial
        cookies = self.driver.get_cookies()  # Captura os cookies
        for cookie in cookies:
            self.driver.add_cookie(cookie)  # Adiciona cookies ao navegador

        # Inicializa uma variável de controle de página
        current_page = 1
        max_pages = 15  # Defina o número máximo de páginas a serem visitadas
        
        while current_page <= max_pages:
            self.logger.info(f"Capturando a página {current_page}")

            # Captura a página atual
            html = self.driver.page_source
            yield scrapy.Request(url=self.driver.current_url, headers=self.get_custom_headers(), callback=self.parse, meta={'html': html})

            # Verifica se há um botão "Próxima Página" e clica nele
            try:
                next_button = self.driver.find_element(By.XPATH, '//button[@aria-label="Go to next page"]')
                if next_button.is_enabled():
                    next_button.click()  # Clica no botão "Próxima Página"
                    current_page += 1  # Incrementa o contador de páginas
                    time.sleep(5)  # Ajuste o tempo conforme necessário
                else:
                    self.logger.info("Botão 'Próxima Página' não está habilitado, encerrando.")
                    break
            except Exception as e:
                self.logger.info("Erro ao tentar clicar no botão 'Próxima Página': {}".format(e))
                break

    def parse(self, response):
        html = response.meta['html']  # Obtém o HTML da meta
        selector = Selector(text=html)
        produtos = selector.css('li.sc-fTyFcS.iTkWie')

        for produto in produtos:
            
            yield {
                'marca': 'Samsung',  # produto.css('span.poly-component__brand::text').get(),
                'titulo': produto.css('h2[data-testid=product-title]::text').get(),
                'preco': produto.css('p[data-testid=price-value]::text').get(),                
                'condicao': 'Usado' if produto.css('h2[data-testid=product-title]::text').get() and "usado" in produto.css('h2[data-testid=product-title]::text').get() else 'Novo',
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
