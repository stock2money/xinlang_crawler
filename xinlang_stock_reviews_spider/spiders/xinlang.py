# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from xinlang_stock_reviews_spider.items import XinlangItem

class XinlangSpider(scrapy.Spider):
    name = 'xinlang'
    allowed_domains = ['weibo.com']
    start_urls = []
    cookies = {
        'SINAGLOBAL': '4322577557836.107.1537703932893',
        '_ga': 'GA1.2.2107160836.1555772042', 
        '_s_tentry': 'finance.sina.com.cn',
        'Apache': '7145756379180.597.1558858424832',
        'ULV': '1558858424854:14:1:1:7145756379180.597.1558858424832:1556114047999',
        'login_sid_t': '17ac25e154399d378498246981fb3345', 
        'cross_origin_proto': 'SSL' ,
        'user_active': '201905262257', 
        'user_unver': '0f06fd88437db26f7f347a520a8c9922', 
        '_gid': 'GA1.2.53602283.1558883509',
        'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W5UPOf-zvNrex5ci70lX92U5JpX5K2hUgL.FoMpSoz01K2E1h-2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMR1hnEeoBXehqf',
        'SSOLoginState': '1558885880',
        'ALF': '1590421901', 
        'SCF': 'AqSz81Ij43vHmt5e8e2jskDyushFQsRbmv-0HNpvku60IImbaLChn28auJ-gVhimtT3JGAo3uKzgmboFoRti_f8.', 
        'SUB': '_2A25x7sZfDeRhGeFP7VAS-S_OwzmIHXVSnbCXrDV8PUNbmtBeLVjHkW9NQQHDiitjc9UfOPFhQvPPvMgLvTmrOzjk', 
        'SUHB': '0mxEq9pSTArx0U',
        'wvr': 6,
        'webim_unReadCount': '%7B%22time%22%3A1558888147326%2C%22dm_pub_total%22%3A0%2C%22chat_group_pc%22%3A0%2C%22allcountNum%22%3A1%2C%22msgbox%22%3A0%7D', 
        'WBStorage': 'e9f7a483794264fd|undefined'
    }

    def __init__(self):
        info = pd.read_csv("data/stocks.csv", header=0, delimiter=",")
        for code in info["code"]:
            code = code[:-4] + 'SH'
            url = "https://s.weibo.com/article?q=" + code + "&Refer=weibo_article"
            self.start_urls.append(url)
    

    def parse(self, response):
        news = response.xpath('//*[@id="pl_feedlist_index"]/div[@class="card-wrap"]/div/div/h3/a')
        for each in news:
            item = XinlangItem()
            item["title"] = each.xpath('@title').extract()[0]
            item["href"] = each.xpath('@href').extract()[0]
            item["code"] = response.url[response.url.index("=")+1:  response.url.index(".SH")] + ".XSHE"
            request = scrapy.Request(url=item["href"], cookies=self.cookies, callback=self.parseHref)
            request.meta['item'] = item
            yield request


    def parseHref(self, response):
        item = response.meta['item']
        item["time"] = response.xpath('//*[@id="plc_main"]/div/div/div/div[2]/div[2]/div[1]/span[2]/text()').extract()[0]
        item["author"] = response.xpath('//*[@id="plc_main"]/div/div/div/div[2]/div[2]/div[1]/span[1]/a/em/text()').extract()[0]
        article = response.xpath('//*[@id="plc_main"]/div/div/div/div[2]/div[3]/p/font')
        detail = ''
        for p in article:
            if len(p.xpath('./text()').extract()) > 0:
                detail += p.xpath('./text()').extract()[0]
        item['detail'] = detail
        # print(detail)
        yield item
