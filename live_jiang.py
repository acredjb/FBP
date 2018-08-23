# -*- coding: utf-8 -*-
# scrapy crawl PL -o BaseData.csv
import datetime
import sys
import requests
import scrapy
import time
import json
import scrapy.http
from peilv.items import PeilvItem

wl_url = 'http://www.jczj123.com/lottery/jczq/jczqSpfHhgg.htm'#wl未来

ls_url= 'http://www.jczj123.com/lottery/jczq/jczqSpfHhggRaceEventReview.htm?gameStartDate='

plurl = 'http://ftapi.jczj123.com/home/service.json?service=HUNDRED_EUR_ODDS_QUERY&'

sp="zhu"

# sp="ke"
if sp=="zhu" :
    sp_pl = 'fho'
else:
    sp_pl = 'fgo'
class LiveJiangSpider(scrapy.Spider):
    name = 'PL'
    allowed_domains = ['jczj123.com']
    def start_requests(self):
        print('--------------into start_requests-----------------')
        # chrome F12 get cookies
        cookie={'_tracker_global_id':'20180512140947gef14f4a170034e69abb54f0748060244',
        'loginInfo':'PQk45OzQkCSqwvkv4Q1ROPPKv0Rchnl2CRbLFXjPucYaaCj4TIt0uNM8UALyqZzyTZK3c1TWgRnkzfqn1lrxZg==',
        'jczjsid':'20180606222a43bfe622cc485fa70123234d39ef6a48faca59',
        'jczjsid_sn':'4751f9ed5989b031d4a564b3cb24069f',
        'cookie':'1.1.6.f4977bf8',
        'Hm_lvt_100743a90fea504059524b1e12c43dc0':'1526105421,1527692227,1528295078',
        'Hm_lpvt_100743a90fea504059524b1e12c43dc0':'1528295078',
        'buriedData':'screen%3A1366X768%7CuserId%3A8201705191571863',
        'JSESSIONID':'687A630E717FF60B2FDA3A86BA54AD6D.jchweb-1-6'}
        # return [scrapy.http.FormRequest(s_url, cookies=cookie, callback=self.parseBefore)]

        today = datetime.date.today()
        
        m = 54
        n = 55 
        
        for d_i in range(m,n):
            oneday = datetime.timedelta(days=d_i)  # 一天
            d1 = str(today - oneday)
            
            d1='2018-08-22'
            request = scrapy.http.FormRequest(wl_url, cookies=cookie,
                                            callback=self.parseBefore, meta={'d1': d1})
            # 
            # d1='2018-07-27'
            # request = scrapy.http.FormRequest(ls_url + d1, cookies=cookie,
            #                                 callback=self.parseBefore, meta={'d1': d1})#传递参数d1到parseBefore中
            yield request

         
        print('-----------out start_requests------------------')
    def parseBefore(self,response):

        print('---------------into parseBefore-----------------')
        d2=response.meta['d1'].replace('-', '')
        racelist=[e5.split("'") for e5 in response.xpath('//tr[@data-isn='+d2+']/@data-inid').extract()]
        for raceid in racelist:
            sel = response.xpath
            item = PeilvItem()
            item['cc'] =str(sel('//tr[@data-inid=' + raceid[0] + ']/@data-isn').extract()[0] + sel('//tr[@data-inid=' + raceid[0] + ']/td[@data-action="hide"'+']/@title').extract()[0])
            bshrefstr = 'http://ft.jczj123.com/race/jump/'+ raceid[0] +'.htm'
            item['bstype'] = str(sel("//a[@href='"+bshrefstr + "']/text()").extract())

            hrefstr='http://ft.jczj123.com/race/seasonRaceEvent.htm?raceId='+ raceid[0]
            score =[e6.split(":") for e6 in  sel("//a[@href='"+hrefstr + "']/text()").extract()]
            for s in score:
                zhu_score = s[0]
                ke_score = s[1]
                if sp == 'zhu':
                    if int(zhu_score) > int(ke_score):
                        item['res'] = 'y'
                    else:
                        item['res'] = 'n'
                if sp == 'ke':
                    if int(ke_score) > int(zhu_score):
                        item['res'] = 'y'
                    else:
                        item['res'] = 'n'
            print('{-------------------for every raceid dealing  item -------------')
            request = scrapy.http.FormRequest(plurl,
                                        formdata={'raceId': raceid},
                                        callback=self.parse,meta={'item':item})
       
            print(raceid)
            print('----------------before yield requests-------------')
            yield request 
            print('---------------end one raceid -------------}')
            #add by daijingbo 20180606

    def parse(self, response):
        # add 20180527
        print('--------------into parse----------------------')
        item = response.meta['item']
       
        t = response.body.decode('utf-8')
        
        odd=0
        li=0
        b5=0
        inte=0
        wl=0
        w=0
        ao=0
        b10=0
        lis = s["response"]["eurList"];
        for i in range(50):
            if i>=1 and (lis[i]['cn']=="澳门" or lis[i]['cn']=="10Bet" or lis[i]['cn']=="Oddset" or lis[i]['cn']=="立博" or lis[i]['cn']=='bet 365' or lis[i]['cn']=='Interwetten' or lis[i]['cn']=='威廉希尔' or lis[i]['cn']=='伟德'):
                # print('------------------into for 160 peilv check 10 peilv---------------------')
                
                if lis[i]['cn'] == "澳门":
                    ao = lis[i][sp_pl]
                if lis[i]['cn'] == "10Bet":
                    b10 = lis[i][sp_pl]
                if lis[i]['cn'] == "Oddset":
                    odd = lis[i][sp_pl]
                if lis[i]['cn'] == "立博":
                    li = lis[i][sp_pl]
                if lis[i]['cn'] == "bet 365":
                    b5 = lis[i][sp_pl]
                if lis[i]['cn'] == "Interwetten":
                    inte = lis[i][sp_pl]
                if lis[i]['cn'] == "威廉希尔":
                    wl = lis[i][sp_pl]
                if lis[i]['cn'] == "伟德":
                    w = lis[i][sp_pl]
        item['ao'] = ao
        item['b10'] = b10
        item['odd'] = odd
        item['li'] = li
        item['b5'] =b5
        item['inte'] = inte
        item['wl'] = wl
        item['w'] = w
        print(odd)
        if w>=2.5 or 0<w<1.4 or odd>=2.5 or 0<=odd<1.3 :
            pass
        else:
            yield item
        print('-----------------out parse----------------------')

