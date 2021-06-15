import bs4
import requests
# -*- coding: UTF-8 -*-

def get_resource(url):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
               "AppleWebKit/537.36 (KHTML, like Gecko)"
               "Chrome/63.0.3239.132 Safari/537.36"}
    return requests.get(url, headers=headers) 

def get_rate_info(stockid):
    urls = []
    Q1_Q2_Q3 = [20211,20183,20161]
    for i in range(3):
        url = "https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR&STOCK_ID="+str(stockid)+"&QRY_TIME="+str(Q1_Q2_Q3[i])
        urls.append(url)
    for url in urls:
        r = get_resource(url)
        r.encoding = "utf-8"
        if r.status_code == requests.codes.ok:
            soup = bs4.BeautifulSoup(r.text, "lxml")
            pro = ["營業毛利率","營業利益率","稅後淨利率","股東權益報酬率(當季)","每股稅後盈餘(元)"]
            man = "營收季成長率"
            sol = "負債總額(%)"
            prof = ["None"]*5
            management_capacity = "None"
            solvency = "None"
            c = soup.find(id="divFinDetail")
            te = c.select("tr")[0].select("td")
            for i in range(len(te)-1):
                try:
                    quarter = te[i+1].select_one('nobr').text
                    for j in range(len(c.select("tr"))):
                        temp = c.select("tr")[j].select("td")[0].select_one('nobr').text
                        temp = temp.replace("\xa0","")
                        for k in range(5):
                            if pro[k] == temp:
                                prof[k] = c.select("tr")[j].select("td")[i+1].select_one('nobr').text
                        if man == temp:
                            management_capacity = c.select("tr")[j].select("td")[i+1].select_one('nobr').text
                        if sol == temp:
                            solvency = c.select("tr")[j].select("td")[i+1].select_one('nobr').text
                    profitability = {                       #獲利能力
                        "gross_margnin" : prof[0],          #營業毛利率
                        "profit_rate" : prof[1],            #營業利益率
                        "net_interest_rate" : prof[2],      #稅後淨利率
                        "shareholders_equity" : prof[3],    #股東權益報酬率(當季)
                        "earning_after_tax" : prof[4]       #每股稅後盈餘(元)
                        }
                    all_rate = {
                        "quarter" : quarter,                            #季別
                        "profitability" : profitability,                #獲利能力
                        "management_capacity" : management_capacity,    #資產季成長率
                        "solvency" : solvency                           #負債總額(%)
                        }
                    print(all_rate)
                except:
                    break
if __name__ == "__main__":
    get_rate_info(2330)