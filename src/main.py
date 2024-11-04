from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader

class Main:
    def __init__(self):
        # Configurações do projeto Scrapy
        self.settings = get_project_settings()
        self.spider_loader = SpiderLoader(self.settings)
        self.process = CrawlerProcess(self.settings)

    def run_all_spiders(self):
        # Executa cada spider e configura o caminho do arquivo JSON manualmente
        for spider_name in self.spider_loader.list():
            spider_cls = self.spider_loader.load(spider_name)
            output_file = f'../../data/{spider_name}_output.json'
            self.process.crawl(spider_cls, custom_settings={
                'FEEDS': {
                    output_file: {
                        'format': 'json',
                        'encoding': 'utf8',
                        'store_empty': False,
                        'indent': 4,
                    }
                }
            })

        # Inicia o processo Scrapy para rodar todos os spiders
        self.process.start()

if __name__ == '__main__':
    main = Main()
    main.run_all_spiders()