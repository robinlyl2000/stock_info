from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
import datetime
from time import mktime
import base64
from requests import request
import json

sp = {'date':'123', 'volume':0, 'open':0.0, 'high':0.0, 'low':0.0, 'close':0.0, 'change':0.0, 'change_rate':0.0}

app_id = 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'
app_key = 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }

### 存取測試檔案
# with open('resource/2330.json',encoding = 'utf8') as f:
#     data = json.load(f)
#     f.close()

def getdays(data):
    data_d = []
    for i in data["data"]["content"]["rawContent"]["day"]:
        stock = dict(sp)
        stock['date'] = i["date"]
        stock['volume'] = i["volume"]
        stock['open'] = i["open"]
        stock['close'] = i["close"]
        stock['high'] = i["high"]
        stock['low'] = i["low"]
        stock['change'] = i["change"]
        if "change_rate" in data["data"]["content"]["rawContent"]["day"][len(data_d)]:
            stock['change_rate'] = i["change_rate"]
        else:
            stock['change_rate'] = "null"
        data_d.append(stock)

    return data_d


def getweeks(data):
    data_w = []
    for i in data["data"]["content"]["rawContent"]["week"]:
        stock = dict(sp)
        stock['date'] = i["date"]
        stock['volume'] = i["volume"]
        stock['open'] = i["open"]
        stock['close'] = i["close"]
        stock['high'] = i["high"]
        stock['low'] = i["low"]
        stock['change'] = i["change"]
        if "change_rate" in data["data"]["content"]["rawContent"]["week"][len(data_w)]:
            stock['change_rate'] = i["change_rate"]
        else:
            stock['change_rate'] = "null"
        data_w.append(stock)

    return data_w

def getmonths(data):
    data_m = []
    for i in data["data"]["content"]["rawContent"]["month"]:
        stock = dict(sp)
        stock['date'] = i["date"]
        stock['volume'] = i["volume"]
        stock['open'] = i["open"]
        stock['close'] = i["close"]
        stock['high'] = i["high"]
        stock['low'] = i["low"]
        stock['change'] = i["change"]
        if "change_rate" in data["data"]["content"]["rawContent"]["month"][len(data_m)]:
            stock['change_rate'] = i["change_rate"]
        else:
            stock['change_rate'] = 'null'
        data_m.append(stock)
    
    return data_m

def connect(input_id, auth):
    response = request('get', 'https://api.fintechspace.com.tw/history/api/v2/data/contents/FCNT000002?symbol_id={id}'.format(input_id), headers= auth.get_auth_header())
    data = json.loads(response.text)
    return json.dumps(
        {
            'id' : input_id,
            'days' : getdays(data),
            'weeks' : getweeks(data),
            'months' : getmonths(data)
        }
    )

if __name__ == '__main__':
    a = Auth(app_id, app_key)
    input_id = input('輸入欲查詢之代碼：')
    result = connect(input_id= str(input_id), auth= a)

### 主要回傳函式
# def getdailydata(id):
#     return json.dumps(
#         {
#             'id' : id,
#             'days' : getdays(),
#             'weeks' : getweeks(),
#             'months' : getmonths()
#         }
#     )

