# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from xinlang_stock_reviews_spider.items import XinlangItem
from scrapy.http import Request

class XinlangSpider(scrapy.Spider):
    name = 'xinlang'
    allowed_domains = ['weibo.com']
    review_urls = []
    xinlang_url = "https://finance.sina.com.cn/stock/"

    def __init__(self):
        info = pd.read_csv("data/stocks.csv", header=0, delimiter=",")
        for code in info["code"][:1]:
            code = code[:-4] + 'SH'
            url = "https://s.weibo.com/article?q=" + code + "&Refer=weibo_article"
            self.review_urls.append(url)

    # 用start_requests()方法,代替start_urls
    def start_requests(self):
        """第一次请求一下登录页面，设置开启cookie使其得到cookie，设置回调函数"""
        return [Request(self.xinlang_url, meta={'cookiejar': 1}, callback=self.parse)]


    def parse(self, response):
         for url in self.review_urls:
            request = scrapy.Request(url=url, meta={'cookiejar': response.meta['cookiejar']}, callback=self.parseUrl)
            yield request

    def parseUrl(self, response):
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
        print(item)
        yield item
