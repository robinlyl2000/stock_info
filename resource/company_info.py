import bs4
import requests
import json
# -*- coding: UTF-8 -*-

def get_resource(url):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
               "AppleWebKit/537.36 (KHTML, like Gecko)"
               "Chrome/63.0.3239.132 Safari/537.36"}
    return requests.get(url, headers=headers) 

def get_company_info(stockid):
    url = "https://goodinfo.tw/StockInfo/BasicInfo.asp?STOCK_ID="+stockid
    r = get_resource(url)
    r.encoding = "utf-8"
    if r.status_code == requests.codes.ok:
        soup = bs4.BeautifulSoup(r.text, "lxml")
        c = soup.body.find_all("table")[15].select("tr")
        a = ["None"]*12
        company = ["公司名稱","產業別","上市/上櫃","資本額","成立日期","上市日期","董事長","總經理","發言人","總機電話","公司網址","主要業務"]
        for i in range(len(c)):
            temp = c[i].select("td")
            if len(temp)!=1:
                for j in range(12):
                    if temp[0].text == company[j]:
                        temp1 = temp[1].text.replace("\xa0","")
                        a[j] = temp1
            if len(temp)==4:
                for j in range(12):
                    if temp[2].text == company[j]:
                        temp1 = temp[3].text.replace("\xa0","")
                        a[j] = temp1
        company_info = json.dumps({
            "公司名稱" : a[0],      #公司名稱
            "產業別" : a[1],          #產業別
            "上市/上櫃" : a[2],    #上市/上櫃
            "資本額" : a[3],           #資本額
            "成立日期" : a[4],        #成立日期
            a[2]+"日期" : a[5],       #上市/上櫃日期
            "董事長" : a[6],          #董事長
            "總經理" :a[7],            #總經理
            "發言人" : a[8],         #發言人
            "總機電話" : a[9],             #總機電話
            "公司網址" : a[10],              #公司網址
            "主要業務" : a[11]    #主要業務
            })
        return company_info