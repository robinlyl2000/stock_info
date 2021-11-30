import bs4
import requests
import json

def clean(str):
    if(str[0] == '(' and str[-1] == ')'):
        str = str[1:-1]
        return '-{}'.format(str)
    return str

def get_resource(url):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
               "AppleWebKit/537.36 (KHTML, like Gecko)"
               "Chrome/63.0.3239.132 Safari/537.36"}
    return requests.get(url, headers=headers) 

def get_stock_info(stockid):
    ymqs = ["2021Q1","2020Q4","2020Q3","2020Q2","2020Q1","2019Q4","2019Q3","2019Q2","2019Q1"]
    urls = []
    for ymq in ymqs:
        url = "https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID="+stockid+"&SYEAR="+ymq[0:4]+"&SSEASON="+ymq[-1]+"&REPORT_ID=C"
        urls.append(url)
    balance = []
    income = []
    money = []
    for url in urls:
        r = get_resource(url)
        r.encoding = "utf-8"
        if r.status_code == requests.codes.ok:
            soup = bs4.BeautifulSoup(r.text, "lxml")
            ba = ["None"]*15
            inc = ["None"]*10
            mo = ["None"]*6          
            try:
                bss = ["1XXX","11XX","1100","1170","1180","1210","130X","1550","1600","1780","1840","1900","2XXX","21XX","2570"]
                ins = ["4000","5000","5900","6000","6900","7000","7900","7950","8200","9750"]
                mf = ["AAAA","BBBB","CCCC","EEEE","E00100","E00200"]
                bass = soup.find_all("table")[0]
                baid = bass.select("tr")
                for i in range(2,len(baid)):
                    for j in range(15):
                        if bss[j] == baid[i].select("td")[0].text:
                            ba[j] = baid[i].select("td")[2].text
                incs = soup.find_all("table")[1]
                incid = incs.select("tr")
                for i in range(2,len(incid)):
                    for j in range(10):
                        if ins[j] == incid[i].select("td")[0].text:
                            inc[j] = incid[i].select("td")[2].text
                mof = soup.find_all("table")[2]
                mofid = mof.select("tr")
                for i in range(2,len(mofid)):
                    for j in range(6):
                        if mf[j] == mofid[i].select("td")[0].text:
                            mo[j] = mofid[i].select("td")[2].text
            except:
                break
            balance_sheet_statement = {
                "1XXX" : clean(ba[0]),     #資產總計 A
                "11XX" : clean(ba[1]),     #流動資產合計 flowA
                "1100" : clean(ba[2]),     #透過損益按公允價值衡量之金融資產 - 流動
                "1170" : clean(ba[3]),     #應收帳款淨額
                "1180" : clean(ba[4]),     #應收帳款 - 關係人淨額
                "1210" : clean(ba[5]),     #其他應收款 - 關係人
                "130X" : clean(ba[6]),     #存貨
                "1550" : clean(ba[7]),     #採用權益法之投資
                "1600" : clean(ba[8]),     #不動產、廠房及設備
                "1780" : clean(ba[9]),     #無形資產
                "1840" : clean(ba[10]),     #遞延所得稅資產
                "1900" : clean(ba[11]),     #其他非流動資產
                "2XXX" : clean(ba[12]),     #負債總計 L
                "21XX" : clean(ba[13]),     #流動負債合計 flowL
                "2570" : clean(ba[14]),      #遞延所得稅負債
            }
            income_statement = {
                "4000" : clean(inc[0]),    #營業收入合計
                "5000" : clean(inc[1]),    #營業成本合計
                "5900" : clean(inc[2]),    #營業毛利(毛損) 1
                "6000" : clean(inc[3]),    #營業費用合計
                "6900" : clean(inc[4]),    #營業利益(損失) 2
                "7000" : clean(inc[5]),    #營業外收入及支出合計
                "7900" : clean(inc[6]),    #繼續營業單位稅前(淨損)
                "7950" : clean(inc[7]),    #所得稅費用(利益)合計
                "8200" : clean(inc[8]),    #本期淨利(淨損) 3
                "9750" : clean(inc[9])     #基本每股盈餘合計
            }
            money_flow = {
                "AAAA" : clean(mo[0]),     #營業活動之淨現金流入(流出)
                "BBBB" : clean(mo[1]),     #投資活動之淨現金流入(流出)
                "CCCC" : clean(mo[2]),     #籌資活動之淨現金流入(流出)
                "EEEE" : clean(mo[3]),     #本期現金及約當現金增加(減少)數
                "E00100" : clean(mo[4]),   #期初現金及約當現金餘額
                "E00200" : clean(mo[5])    #期末現金及約當現金餘額
            }
            # A : 1100
            # B : 1170+1180+1210
            balance.append(balance_sheet_statement)
            income.append(income_statement)
            money.append(money_flow)
    all_info = {}
    for i in range(len(ymqs)):
        all_info[ymqs[i]] = {
            "balance_sheet_statement" : balance[i],   #資產負債表
            "income_statement" : income[i],           #損益表
            "money_flow" : money[i]                   #現金流量表
        }
    return json.dumps(all_info)
            
            
if __name__ == "__main__":
    get_stock_info('2330')


        
