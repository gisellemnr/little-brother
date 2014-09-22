# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from little_brother.items import DeputyItem

class LittleBrotherSpider(CrawlSpider):
    name = "little_brother"
    allowed_domains = ["camara.gov.br"]
    start_urls = (
        #This list should contain all the deputies from this period of thime (legislatura 54) -- change this number to get deputies from other periods
        'http://www.camara.gov.br/internet/deputado/Dep_Lista.asp?Legislatura=54&Partido=QQ&SX=QQ&Todos=None&UF=QQ&condic=QQ&forma=lista&nome=&ordem=nome&origem=None',
        #Example: 'http://www.camara.leg.br/Internet/Deputado/dep_Detalhe.asp?id=141463',
    )
    rules = ( Rule(LxmlLinkExtractor(allow=(".*Dep_Detalhe\.asp", ),), callback="parse_deputy", follow= True,),\
              Rule(LxmlLinkExtractor(allow=(".*RelVotacoes\.asp", ),), callback="parse_voting",  follow= True, ), 
            )

    def parse_deputy(self, response):
        basic_info = response.xpath("//div[@class='bloco clearedBox']/ul/li")

        item = DeputyItem()
        for sel in basic_info:
            strong = sel.xpath("strong/text()").extract()
            if strong and "nome civil" in strong[0].lower():
                item["name"] = sel.xpath("text()").extract()[0].strip()

            if strong and "partido" in strong[0].lower():
                info = sel.xpath("text()").extract()[0].strip().split("/")
                item["party"] = info[0].strip()
                item["state"] = info[1].strip()
                item["active"] = info[2].strip()

            gid = re.match(".*id=(?P<id>\w*)", response.url)
            item["deputy_id"] = gid.group("id")
            #item["deputy_register"] = 

        yield item

    def parse_voting(self, response):
        print "Parsing:", response.url
        pass
    

    def filter_deputy(self, response):
        pass
    
