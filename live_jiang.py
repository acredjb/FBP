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
# 20180419待解决问题：场次1，2，3；raceId的获取，做循环,20180602解决
#20180604待解决问题：未来比赛（包括当天）取值,20180606解决
#获取当天或未来某天数据的地址
wl_url = 'http://www.jczj123.com/lottery/jczq/jczqSpfHhgg.htm'#wl未来
#获取历史数据的地址
# ls_url = 'http://www.jczj123.com/lottery/jczq/jczqSpfHhggRaceEventReview.htm?gameStartDate=2018-06-03'#ls历史
ls_url= 'http://www.jczj123.com/lottery/jczq/jczqSpfHhggRaceEventReview.htm?gameStartDate='#ls历史
#获取赔率的地址
plurl = 'http://ftapi.jczj123.com/home/service.json?service=HUNDRED_EUR_ODDS_QUERY&'#pl赔率
# plurl = 'http://ftapi.jczj123.com/home/service.json?service=HUNDRED_EUR_ODDS_QUERY&raceId=3840351'#pl赔率
#上盘赔率
sp="zhu"

# sp="ke"
if sp=="zhu" :#上盘为主队赔率
    sp_pl = 'fho'
else:#上盘为客队赔率
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
        # m=40
        # n=51#4.20-4.30有问题
        #52开始是4.19之前
        m = 54 #包含m
        n = 55 #不包含n，315为2017-8-1至2018-6-11的315天
        #m,n:1,4;4,7;7,11;11...间隔3天可以获取全的数据-也需多执行几次，取最多的一次，程序有bug有空调试
        for d_i in range(m,n):#20180604待解决问题：连续N天数据如何取值,20180609解决。range(m,n)获取“今天往前n-1天”至“今天往前m天”共计n-m-1天数据
            oneday = datetime.timedelta(days=d_i)  # 一天
            d1 = str(today - oneday)
            # 未来 wl，#取未来某天的数据，单独手动执行此3行代码
            d1='2018-08-22'
            request = scrapy.http.FormRequest(wl_url, cookies=cookie,
                                            callback=self.parseBefore, meta={'d1': d1})
            # 历史ls，#取历史N-M天的数据执行下边2行代码
            # d1='2018-07-27'
            # request = scrapy.http.FormRequest(ls_url + d1, cookies=cookie,
            #                                 callback=self.parseBefore, meta={'d1': d1})#传递参数d1到parseBefore中
            yield request

         # 通过FromRequest，再通过parseBefore回调函数解析wl_url地址，将此页面的信息通过parseBefore中的response返回来
        print('-----------out start_requests------------------')
    def parseBefore(self,response):
        # http: // www.jb51.net / article / 133687.htm参考
        print('---------------into parseBefore-----------------')
        d2=response.meta['d1'].replace('-', '')#获取传递进来的d1参数2018-06-09转化为20180609作为d2
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
                zhu_score = s[0]#主队得分
                ke_score = s[1]#客队得分
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
                                        formdata={'raceId': raceid},#formdata是添加在plurl后的动态网址
                                        callback=self.parse,meta={'item':item})
            # 通过FromRequest，再通过parse回调函数解析plurl地址，将此页面的信息通过parse中的response返回来
            print(raceid)
            print('----------------before yield requests-------------')
            yield request #并非return，yield压队列，parse函数将会被当做一个生成器使用。scrapy会逐一获取parse方法中生成的结果，并没有直接执行parse，循环完成后，再执行parse
            print('---------------end one raceid -------------}')
            #add by daijingbo 20180606 循环遍历历史日期数据

    def parse(self, response):
        # add 20180527
        print('--------------into parse----------------------')
        item = response.meta['item']
        # t = response.body.decode('UTF8')
        t = response.body.decode('utf-8')
        # with open("jsondata.json", "w") as file:  # 打开一个名为jsondata.json文本，只能写入状态 如果没有就创建
        #     json.dump(t, file)  # data转换为json数据格式并写入文件
        #     file.close()  # 关闭文件
        # print(t)
        # struct={}
        # s=[]
        s = json.loads(t)
        # try:
        #     try:#try parsing to dict
        #         # t=str(t).strip("'<>() ").replace('\'','\"')
        #         s = json.loads(t)
        #         # struct = json.loads(t)
        #     except:
        #         print("--------------repr(t)-----------------------"+repr(t))
        #         print("--------------sys.exc_info()----------------"+sys.exc_info())
        # except:
        #     print("log")
        # s = requests.get(t).complexjson()
        odd=0
        li=0
        b5=0
        inte=0
        wl=0
        w=0
        ao=0
        b10=0
        lis = s["response"]["eurList"];
        for i in range(50):#160，澳门-1，10Bet-27，Oddset-22，立博-4，bet 365-11，Interwetten-19，威廉希尔-7，伟德-8
            if i>=1 and (lis[i]['cn']=="澳门" or lis[i]['cn']=="10Bet" or lis[i]['cn']=="Oddset" or lis[i]['cn']=="立博" or lis[i]['cn']=='bet 365' or lis[i]['cn']=='Interwetten' or lis[i]['cn']=='威廉希尔' or lis[i]['cn']=='伟德'):
                # print('------------------into for 160 peilv check 10 peilv---------------------')
                # 上盘为客队，取上盘为主队时屏蔽下边一行
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
            yield item#程序在取得各个页面的items前，会先处理完之前所有的request队列里的请求，然后再提取items
        print('-----------------out parse----------------------')

