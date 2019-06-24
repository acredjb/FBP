# -*- coding: utf-8 -*-
# scrapy crawl FBP -o BaseData.csv
import datetime
import sys
import requests
import scrapy
import time
import json
import scrapy.http
from peilv.items import PeilvItem

#获取当天或未来某天数据的地址
wl_url = 'https://live.leisu.com/saicheng?date='#wl历史https://live.leisu.com/saicheng?date=20190620
#获取历史数据的地址
ls_url = 'https://live.leisu.com/wanchang?date='#ls历史https://live.leisu.com/wanchang?date=20190606

class LiveJiangSpider(scrapy.Spider):
    name = 'FBP'
    allowed_domains = ['leisu.com']
    def start_requests(self):
        print('--------------into start_requests-----------------')
        today = datetime.date.today()
        m = 7 #包含m
        n = 8 #不包含n，315为2017-8-1至2018-6-11的315天；20190207可以间隔100天进行数据抓取，m=458，n=558

        for d_i in range(m,n):
            oneday = datetime.timedelta(days=d_i)  # 一天
            d1 = str(today - oneday)
            d1='20190306'
            # d1='20190622'
            # d1 = '2019-06-03'
            # 未来 wl，#取未来某天的数据，单独手动执行此2行代码
            # request = scrapy.http.FormRequest(wl_url + d1,
            #                                 callback=self.parseWl, meta={'d1': d1})
            # 历史ls，#取历史N-M天的数据执行下边2行代码
            request = scrapy.http.FormRequest(ls_url + d1,
                                            callback=self.parseLs, meta={'d1': d1})#传递参数d1到parseBefore中

            yield request
         # 通过FromRequest，再通过parseBefore回调函数解析wl_url地址，将此页面的信息通过parseBefore中的response返回来
        print('-----------out start_requests------------------')
    def parseWl(self,response):
        print('---------------into parseWl-----------------')
        d2=response.meta['d1']
        # print(d2)
        sel=response.xpath
        racelist=[e5.split("'") for e5 in sel('//li[@data-status="1"]/@data-id').extract()]
        for raceid in racelist:#raceid=['2674547'];raceid[0]=2674547
            item = PeilvItem()
            # raceid[0]="2674547"
            sel_div=sel('//*[@data-id=' + str(raceid[0]) + ']/div[@class="find-table layout-grid-tbody hide"]/div[@class="clearfix-row"]')
            if str(sel_div.xpath('span[@class="lab-lottery"]/span[@class="text-jc"]/text()').extract()) == "[]":
                item['cc']=""
            else:
                item['cc']=str(d2) + str(sel_div.xpath('span[@class="lab-lottery"]/span[@class="text-jc"]/text()').extract()[0])

            if "周" in item['cc']:#取竞彩-周一001等
                item['bstype'] = str(sel_div.xpath('span[@class="lab-events"]/a[@class="event-name"]/span["display-i-b w-bar-100 line-h-14 v-a-m lang "]/text()').extract()[0])
                item['res']=''
                plurl='https://live.leisu.com/3in1-'+raceid[0]
                # print('{-------------------for every raceid dealing  item -------------')
                request = scrapy.http.FormRequest(plurl,
                                        # formdata={'raceId': raceid},#formdata是添加在plurl后的动态网址
                                        callback=self.parse,meta={'item':item})
                # # 通过FromRequest，再通过parse回调函数解析plurl地址，将此页面的信息通过parse中的response返回来
                # print('----------------before yield requests-------------')
                yield request #并非return，yield压队列，parse函数将会被当做一个生成器使用。scrapy会逐一获取parse方法中生成的结果，并没有直接执行parse，循环完成后，再执行parse

    def parseLs(self,response):
        print('---------------into parseBefore-----------------')
        d2=response.meta['d1']
        # print(d2)
        sel=response.xpath
        # item['title']=response.xpath('//div[@class="item"]').xpath('div[@class="pic"]/a/img/@alt').extract()#https://blog.csdn.net/circle2015/article/details/53053632
        racelist=[e5.split("'") for e5 in sel('//li[@data-status="8"]/@data-id').extract()]
        for raceid in racelist:#raceid=['2674547'];raceid[0]=2674547
            item = PeilvItem()
            # raceid[0]="2674547"
            sel_div=sel('//li[@data-id='+str(raceid[0])+']/div[@class="find-table layout-grid-tbody hide"]/div[@class="clearfix-row"]')
            if str(sel_div.xpath('span[@class="lab-lottery"]/span[@class="text-jc"]/text()').extract()) == "[]":
                item['cc']=""
            else:
                item['cc']=str(d2) + str(sel_div.xpath('span[@class="lab-lottery"]/span[@class="text-jc"]/text()').extract()[0])
            if "周" in item['cc']:#取竞彩-周一001等
                item['bstype'] = str(sel_div.xpath('span[@class="lab-events"]/a[@class="event-name"]/span["display-i-b w-bar-100 line-h-14 v-a-m lang "]/text()').extract()[0])
                score = str(sel_div.xpath('span[@class="float-left position-r w-300"]/span[@class="lab-score color-red"]/span[@class="score"]/b[@class="color-red skin-color-s"]/text()').extract()[0])
                if score[0:1] > score[2:3] :
                    item['res']='y'
                else:
                    item['res']='n'
                plurl='https://live.leisu.com/3in1-'+raceid[0]
                # print('{-------------------for every raceid dealing  item -------------')
                request = scrapy.http.FormRequest(plurl,callback=self.parse,meta={'item':item})
                # # 通过FromRequest，再通过parse回调函数解析plurl地址，将此页面的信息通过parse中的response返回来
                yield request #并非return，yield压队列，parse函数将会被当做一个生成器使用。scrapy会逐一获取parse方法中生成的结果，并没有直接执行parse，循环完成后，再执行parse

    def parse(self, response):
        print('--------------into parse----------------------')
        item = response.meta['item']
        # t = response.body.decode('utf-8')
        # s = json.loads(t)

        pv=response.xpath
        pl_str = '/td[@class="bd-left"]/div[@class="begin float-left w-bar-100 bd-bottom p-b-8 color-999 m-b-8"]/span[@class="float-left col-3"]/text()'
        # print(str(pv('//*[@data-id="7"]'+pl_str).extract()))
        # 若赔率（ao）暂未给出时会报错IndexError: list index out of range,
        #if else 解决上面问题
        if str(pv('//*[@data-id="7"]'+pl_str).extract())=="[]":
            item['ao'] =  ''
        else:
            item['ao']=pv('//*[@data-id="7"]' + pl_str).extract()[0]
        # item['b10'] = pv('//*[@data-id="4"]/td[@class="bd-left"]/div[@class="begin float-left w-bar-100 bd-bottom p-b-8 color-999 m-b-8"]/span[@class="float-left col-3"]/text()').extract()[0]
        if str(pv('//*[@data-id="4"]'+pl_str).extract())=="[]":
            item['b10'] =  ''
        else:
            item['b10']=pv('//*[@data-id="4"]' + pl_str).extract()[0]

        if str(pv('//*[@data-id="5"]'+pl_str).extract())=="[]":
            item['li'] =  ''
        else:
            item['li']=pv('//*[@data-id="5"]' + pl_str).extract()[0]

        if str(pv('//*[@data-id="2"]'+pl_str).extract())=="[]":
            item['b5'] =  ''
        else:
            item['b5']=pv('//*[@data-id="2"]' + pl_str).extract()[0]

        if str(pv('//*[@data-id="13"]'+pl_str).extract())=="[]":
            item['inte'] =  ''
        else:
            item['inte']=pv('//*[@data-id="13"]' + pl_str).extract()[0]

        if str(pv('//*[@data-id="9"]'+pl_str).extract())=="[]":
            item['wl'] =  ''
        else:
            item['wl']=pv('//*[@data-id="9"]' + pl_str).extract()[0]

        if str(pv('//*[@data-id="11"]'+pl_str).extract())=="[]":
            item['w'] =  ''
        else:
            item['w']=pv('//*[@data-id="11"]' + pl_str).extract()[0]

        if str(pv('//*[@data-id="6"]'+pl_str).extract())=="[]":
            item['ms'] =  ''
        else:
            item['ms']=pv('//*[@data-id="6"]' + pl_str).extract()[0]

        if str(pv('//*[@data-id="10"]'+pl_str).extract())=="[]":
            item['ysb'] =  ''
        else:
            item['ysb']=pv('//*[@data-id="10"]' + pl_str).extract()[0]

        if str(pv('//*[@data-id="3"]'+pl_str).extract())=="[]":
            item['hg'] =  ''
        else:
            item['hg']=pv('//*[@data-id="3"]' + pl_str).extract()[0]

        if str(pv('//*[@data-id="22"]'+pl_str).extract())=="[]":
            item['pin'] =  ''
        else:
            item['pin']=pv('//*[@data-id="22"]' + pl_str).extract()[0]

        if str(pv('//*[@data-id="8"]'+pl_str).extract())=="[]":
            item['sna'] =  ''
        else:
            item['sna']=pv('//*[@data-id="8"]' + pl_str).extract()[0]

################yield######################

        if item['b5']=='' or float(item['b5']) < 1.45 or float(item['b5']) > 2.45:
            pass
        else:
            yield item#程序在取得各个页面的items前，会先处理完之前所有的request队列里的请求，然后再提取items
        print('-----------------out parse----------------------')

