# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from News_scrapy.items import RsarxivItem


class Syncedreview(CrawlSpider):
    # 爬虫名
    name = "rsarxiv"
    # 爬取域范围, 允许爬虫在这个域名下进行爬取
    allowed_domains = ["rsarxiv.github.io"]
    # 起始url列表, 爬虫执行后的第一批请求, 队列处理
    start_urls = ['http://rsarxiv.github.io/']


    rules = (
        # 从起始页提取匹配正则式'/channel/\d{1,3}\.html'的链接，并使用parse来解析
        Rule(LxmlLinkExtractor(allow=(r'/tags/.+/', )), follow=True),
        # 提取匹配'/article/[\d]+.html'的链接，并使用parse_item_yield来解析它们下载后的内容，不递归
        Rule(LxmlLinkExtractor(allow=(r'/\d{4}/\d{2}/\d{2}/.+/', )), callback='parse_item'),
    )


    def parse_item(self, response):
        item = RsarxivItem()
        item['url'] = response.url
        item['title'] = response.xpath('//*[@id="wrapper"]/article/div/header/h1/text()').extract()[0].strip()
        item['pub_time'] = response.xpath('//*[@id="wrapper"]/article/div/header/time/a/text()').extract()[0].strip()
        item['content_code'] = response.xpath('//*[@id="wrapper"]/article/div/div').extract()[0].strip()

        # 返回每个提取到的item数据, 给管道文件处理, 同时还会回来执行后面的代码
        yield item