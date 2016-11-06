#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import scrapy
from p2pblack.items import P2PblackItem
import re

class P2pSpider(scrapy.Spider):
    name = "p2p"
    allowed_domains = ["p2pblack.com"]
    start_urls = (
        'http://www.p2pblack.com/cheat/frontDeadBeatList.html?currentPage=1&showCount=20',
        'http://www.p2pblack.com/cheat/frontDeadBeatList.html?currentPage=43&showCount=20',
    )

    def parse(self, response):
        for i in response.xpath('//div[@class="ft_publick_pzxxright ft_publick_myjb"]'):
            item = P2PblackItem()
            if i.xpath('p[1]/text()').extract()[0].split('：')[-1].strip():
                item['name'] = i.xpath('p[1]/text()').extract()[0].split('：')[-1].strip()
            else:
                pass
            #item['name'] = i.xpath('p[1]/text()').extract()[0].split('：')[-1].strip()

            if i.xpath('p[2]/text()').extract()[0].split('老赖联系方式：')[1:][0].rstrip() :
                item['lianxi'] = i.xpath('p[2]/text()').extract()[0].split('老赖联系方式：')[1:][0].rstrip()
            else :
                pass
            #item['lianxi']=i.xpath('p[2]/text()').extract()[0].split('老赖联系方式：')[1:][0].rstrip()

            if i.xpath('p[3]/text()').extract()[0].split('：')[-1].strip() :
                item['id'] = i.xpath('p[3]/text()').extract()[0].split('：')[-1].strip()
            else :
                pass
            #item['id'] = i.xpath('p[3]/text()').extract()[0].split('：')[-1].strip()

            # item['sex']=int(i.xpath('p[3]/text()').extract()[0].split('：')[-1][-2])%2
            # if int(i.xpath('p[3]/text()').extract()[0].split('：')[-1][-2])%2 == 0:
            #     item['sex'] = "女"
            # else:
            #     item['sex'] = "男"
            #item['sex'] = "女" if int(i.xpath('p[3]/text()').extract()[0].split('：')[-1][-2])%2 == 0 else  "男"
            yield item

        next_page = response.xpath('//ul/li[11]/a/@onclick').re('\d+')
        print(next_page)
        if next_page is not None:
            # response.url.split('?')[0] +"?page="+next_page[0]
            next_page_url = response.url.split('?')[0] +"?currentPage=" + next_page[0] + "&showCount=20"
            yield scrapy.Request(next_page_url, callback=self.parse)

