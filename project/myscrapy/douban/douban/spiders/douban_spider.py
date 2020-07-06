# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名
    name = 'douban_spider'
    allowed_domains = ['movie.douban.com']
    # 入口url
    start_urls = ['https://movie.douban.com/top250']

    # 默认解析方法
    def parse(self, response):
        # print(response.text.encode('gb18030'))
        # print(response.text)
        item_list = response.xpath(u"//div[@class='article']//li")
        for item in item_list:
            book = DoubanItem()
            book['serial_num'] = item.xpath(u".//em/text()").extract_first()
            book['movie_name'] = item.xpath(u".//a/span[1]/text()").extract_first()
            content = item.xpath(u".//div[@class='bd']/p[1]/text()").extract()
            intro_list = []
            for tmp in content:
                intro_list.append(''.join(tmp.strip("'").split()))
            book['introduction'] = intro_list[0] + intro_list[1]

            book['star'] = item.xpath(u".//span[@class='rating_num']/text()").extract_first()
            book['evaluate'] = item.xpath(u".//div[@class='bd']/div/span[last()]/text()").extract_first()
            book['description'] = item.xpath(u".//p[@class='quote']//span/text()").extract_first()
            # print(book)
            yield book

        # 取后页直到解析全部数据
        next_url = response.xpath(u"//span[@class='next']/a/@href").extract()
        if next_url:
            next_url = 'https://movie.douban.com/top250' + next_url[0]
            # yield scrapy.Request(next_url, callback=self.parse)

