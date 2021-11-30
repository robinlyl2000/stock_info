import json



sp = {'date':'123', 'volume':0, 'open':0.0, 'high':0.0, 'low':0.0, 'close':0.0, 'change':0.0, 'change_rate':0.0, 'ma5':0.0, 'ma10':0.0, 'ma20':0.0, 'volma5':0.0, 'volma10':0.0,}

def get_day_week_month(data):
    stock_data = [[],[],[]]
    dwm = ["day","week","month"]
    for x in range(3):
        count = 1
        for i in data["data"]["content"]["rawContent"][dwm[x]]:
            stock = dict(sp)
            stock['date'] = i["date"]
            stock['volume'] = i["volume"]
            stock['open'] = i["open"]
            stock['close'] = i["close"]
            stock['high'] = i["high"]
            stock['low'] = i["low"]
            stock['change'] = i["change"]
            if "change_rate" in data["data"]["content"]["rawContent"][dwm[x]][len(stock_data[x])]:
                stock['change_rate'] = i["change_rate"]
            else:
                stock['change_rate'] = 'null'
            # 判斷ma值
            temp = get_ma(data,count,dwm[x])
            stock['ma5'] = temp[0][0]
            stock['volma5'] = temp[1][0]
            stock['ma10'] = temp[0][1]
            stock['volma10'] = temp[1][1]
            stock['ma20'] = temp[0][2]
            stock['id'] = count
            count = count + 1
            stock_data[x].append(stock)
    return stock_data

def getchange(data):
    output = { 'today' : 0.0, 'one' : 0.0, 'three' : 0.0, 'six' : 0.0}
    temp = 0
    close = 0.0
    one = 0.0
    three = 0.0
    six = 0.0
    # 抓最新資料的id和收盤價和變動比率
    for i in data:
        if i['id'] > temp:
            temp = i['id']
            close = i['close']
            output['today'] = i['change_rate']
    # 計算一個月、三個月、半年的變動比率
    for i in data:
        if i['id'] == temp - 30:
            one =i['close']
        if i['id'] == temp - 90:
            three = i['close']
        if i['id'] == temp - 120:
            six = i['close']
    # 賦值
    output['one'] = (close - one)/one * 100
    output['three'] = (close - three)/three * 100
    output['six'] = (close - six)/six * 100
    return output

def getdailydata(id):

    with open('resource/{}.json'.format(id),encoding = 'utf8') as f:
        data = json.load(f)
        f.close()

    result = {}
    result["id"] = id
    day_week_month = get_day_week_month(data=data)
    result["days"] = day_week_month[0]
    result["weeks"] = day_week_month[1]
    result["months"] = day_week_month[2]
    result["change"] = getchange(data= result["days"])
    return json.dumps(
        {
            'id' : id,
            'days' : result["days"],
            'weeks' : result["weeks"],
            'months' : result["months"],
            'change' : result["change"]
        }
    )

def getdailyrate(input):
    with open('resource/company_id.json',encoding = 'utf8') as f:
        companyid = json.load(f)
        f.close()

    result = []
    for i in input:
        temp = {}
        with open('resource/{}.json'.format(i),encoding = 'utf8') as f:
            data = json.load(f)
            f.close()
        day_week_month = get_day_week_month(data=data)
        t = day_week_month[0]
        temp["id"] = i
        temp["name"] = companyid[i]
        temp["close"] = getlastestchange(t)[0]
        temp["change_rate"] = getlastestchange(t)[1]
        result.append(temp)

    return json.dumps(result)

def getlastestchange(data):
    count = 0
    close = ''
    change_rate = ''
    for i in data:
        if i["id"] > count:
            close =i["close"]
            change_rate = i["change_rate"]
            count = i["id"]
    return  [close, change_rate]
    
        

def get_ma(data,count,dwm):
    num = [5,10,20]
    temp = [[0.0]*3 for j in range(2)]
    for j in range(3):
        if count >= num[j]:
            for k in range(num[j]):
                temp[0][j] += data["data"]["content"]["rawContent"][dwm][count-k-1]["close"]
                temp[1][j] += data["data"]["content"]["rawContent"][dwm][count-k-1]["volume"]
            temp[0][j] /= float(num[j])
            temp[1][j] /= float(num[j])
        else:
            temp[0][j] = 0.0
            temp[1][j] = 0.0
    return temp
