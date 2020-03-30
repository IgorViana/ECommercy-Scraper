# coding=UTF-8
import scrapy


class OfertasSpider(scrapy.Spider):
    name= 'ofertas'

    start_urls= [
        'https://www.magazineluiza.com.br/'
    ]

    def parse(self, response):
        
        ofertas = response.xpath("//li[@class='item-of-menu item-two js-item']/a/@href").extract_first()
        if ofertas is not None:
            ofertas_link = response.urljoin(ofertas)
            yield scrapy.Request(url= ofertas_link, callback=self.parse_ofertas)
            
       

    def parse_ofertas(self, response):
        for oferta in response.xpath("//ul[@role='main']/a"):
            descricao= oferta.xpath(".//div/h3/text()").extract()
            preco= oferta.xpath("./div/div[2]/div[2]/text()").extract_first()
            if preco is None:
                preco = oferta.xpath("./div/div[2]/div[2]/span/text()").extract_first()

            yield {
            'descricao': descricao ,
            'preco': preco}

        index = 1
        for paginas in response.xpath("//ul[@class='css-9j990n']/li/a/text()"):
            if paginas is not None:
                index = index + 1
                page_url = "?page={}".format(index)
                next_page_link = response.urljoin(page_url)
                yield scrapy.Request(url= next_page_link, callback=self.parse_ofertas)