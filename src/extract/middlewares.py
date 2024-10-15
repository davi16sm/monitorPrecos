# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

import random
import requests
import json
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ExtractSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ExtractDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

class RotateUserAgentMiddleware(UserAgentMiddleware):
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        # Add more user agents...
    ]

    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(crawler.settings.get('USER_AGENT'))
        crawler.signals.connect(obj.spider_opened, signal=signals.spider_opened)
        return obj

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agents)
        request.headers['User-Agent'] = user_agent

  

class ScrapedoProxyMiddleware:
    def __init__(self, proxy_url):
        self.proxy_url = proxy_url
        self.proxy_list = self.load_proxies()

    @classmethod
    def from_crawler(cls, crawler):
        # Pega a URL do JSON de proxies a partir das configurações
        proxy_url = crawler.settings.get('PROXY_URL')
        return cls(proxy_url)

    def load_proxies(self):
        """Faz a requisição ao serviço de proxy e carrega a lista de proxies."""
        try:
            response = requests.get(self.proxy_url)
            response.raise_for_status()
            # Extrai os proxies do JSON, apenas os que estão ativos (alive: true)
            proxies = response.json().get('proxies', [])
            # Filtra apenas proxies com protocolos http ou https
            return [proxy for proxy in proxies if proxy.get('alive', False) and proxy.get('protocol') in ['http', 'https']]
        except requests.RequestException as e:
            print(f"Erro ao carregar proxies: {e}")
            return []

    def process_request(self, request, spider):
        if not self.proxy_list:
            # Se a lista de proxies está vazia, tente recarregar
            self.proxy_list = self.load_proxies()

        if self.proxy_list:
            # Escolhe um proxy aleatório da lista
            proxy = random.choice(self.proxy_list)
            
            # Configura o proxy na requisição
            proxy_address = f"{proxy['protocol']}://{proxy['ip']}:{proxy['port']}"
            request.meta['proxy'] = proxy_address
            print(f"Usando proxy: {proxy_address}")
