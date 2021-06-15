import bs4
import requests
# -*- coding: UTF-8 -*-

def get_resource(url):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
               "AppleWebKit/537.36 (KHTML, like Gecko)"
               "Chrome/63.0.3239.132 Safari/537.36"}
    return requests.get(url, headers=headers) 

def get_dividend_info(stockid):
    url = "https://goodinfo.tw/StockInfo/StockDividendPolicy.asp?STOCK_ID="+str(stockid)+"&SHOW_ROTC="
    r = get_resource(url)
    r.encoding = "utf-8"
    if r.status_code == requests.codes.ok:
        soup = bs4.BeautifulSoup(r.text, "lxml")
        year = ["2021","2020","2019","2018","2017","2016"]
        cash_dividend = ["None"]*6
        stock_dividend = ["None"]*6
        all_dividend = ["None"]*6
        c = soup.find(id="divDetail").select("tr")
        for i in range(4,len(c)):
            try:
                for j in range(6):
                    if c[i].select("td")[0].select_one('nobr').select_one("b").text == year[j]:
                        cash_dividend[j] = c[i].select("td")[3].text
                        stock_dividend[j] = c[i].select("td")[6].text
                        all_dividend[j] = c[i].select("td")[7].text
                if all_dividend[5]!="None":
                    break
            except:
                break
        for i in range(6):
            dividend = {
                "year" : year[i],                       #年分
                "cash_dividend" : cash_dividend[i],     #現金股利
                "stock_dividend" : stock_dividend[i],   #股票股利
                "all_dividend" : all_dividend[i]        #合季股利
                }
            print(dividend)
    
if __name__ == "__main__":
    get_dividend_info(2330)