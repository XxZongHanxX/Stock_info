import bs4
import requests
# -*- coding: UTF-8 -*-

def get_resource(url):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
               "AppleWebKit/537.36 (KHTML, like Gecko)"
               "Chrome/63.0.3239.132 Safari/537.36"}
    return requests.get(url, headers=headers) 

def get_stock_info(stockid):
    ymqs = ["2021Q1","2020Q4","2020Q3","2020Q2","2020Q1","2019Q4","2019Q3","2019Q2","2019Q1","2018Q4",
               "2018Q3","2018Q2","2018Q1","2017Q4","2017Q3","2017Q2","2017Q1","2016Q4","2016Q3","2016Q2","2016Q1"]
    urls = []
    for ymq in ymqs:
        url = "https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID="+str(stockid)+"&SYEAR="+ymq[0:4]+"&SSEASON="+ymq[-1]+"&REPORT_ID=C"
        urls.append(url)
    ym = 0
    for url in urls:
        r = get_resource(url)
        r.encoding = "utf-8"
        if r.status_code == requests.codes.ok:
            soup = bs4.BeautifulSoup(r.text, "lxml")
            ba = ["None"]*15
            inc = ["None"]*10
            mo = ["None"]*6          
            stockid_ymq = soup.head.title.text.split(" ")
            if len(stockid_ymq)==5:
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
            elif len(stockid_ymq)==1:
                try:
                    bss = ["資產總計","流動資產合計","透過損益按公允價值衡量之金融資產－流動","應收帳款淨額","應收帳款－關係人淨額",
                           "其他應收款－關係人","存貨","採用權益法之投資","不動產、廠房及設備","無形資產","遞延所得稅資產",
                           "其他非流動資產","負債總計","流動負債合計","遞延所得稅負債"]
                    ins = ["營業收入合計","營業成本合計","營業毛利（毛損）","營業費用合計","營業利益（損失）","營業外收入及支出合計",
                           "繼續營業單位稅前淨利（淨損）","所得稅費用（利益）合計","本期淨利（淨損）","基本每股盈餘合計"]
                    mf = ["營業活動之淨現金流入（流出）","投資活動之淨現金流入（流出）","籌資活動之淨現金流入（流出）",
                          "本期現金及約當現金增加（減少）數","期初現金及約當現金餘額","期末現金及約當現金餘額"]
                    bass = soup.find_all("table")[1]
                    baid = bass.select("tr")
                    for i in range(2,len(baid)):
                        temp = baid[i].select("td")[0].text
                        temp = temp.replace("\u3000","")
                        temp = temp.replace(" ","")
                        for j in range(15):
                            if bss[j] == temp:
                                ba[j] = baid[i].select("td")[1].text
                                ba[j] = ba[j].replace("\u3000","")
                                ba[j] = ba[j].replace(" ","")
                    incs = soup.find_all("table")[2]
                    incid = incs.select("tr")
                    for i in range(2,len(incid)):
                        temp = incid[i].select("td")[0].text
                        temp = temp.replace("\u3000","")
                        temp = temp.replace(" ","")
                        for j in range(10):
                            if ins[j] == temp:
                                inc[j] = incid[i].select("td")[1].text
                                inc[j] = inc[j].replace("\u3000","")
                                inc[j] = inc[j].replace(" ","")
                    mof = soup.find_all("table")[3]
                    mofid = mof.select("tr")
                    for i in range(2,len(mofid)):
                        temp = mofid[i].select("td")[0].text
                        temp = temp.replace("\u3000","")
                        temp = temp.replace(" ","")
                        for j in range(6):
                            if mf[j] == temp:
                                mo[j] = mofid[i].select("td")[1].text
                                mo[j] = mo[j].replace("\u3000","")
                                mo[j] = mo[j].replace(" ","")
                except:
                    break
            balance_sheet_statement = {
                "1XXX" : ba[0],     #資產總計
                "11XX" : ba[1],     #流動資產合計
                "1100" : ba[2],     #透過損益按公允價值衡量之金融資產 - 流動
                "1170" : ba[3],     #應收帳款淨額
                "1180" : ba[4],     #應收帳款 - 關係人淨額
                "1210" : ba[5],     #其他應收款 - 關係人
                "130X" : ba[6],     #存貨
                "1550" : ba[7],     #採用權益法之投資
                "1600" : ba[8],     #不動產、廠房及設備
                "1780" : ba[9],     #無形資產
                "1840" : ba[10],    #遞延所得稅資產
                "1900" : ba[11],    #其他非流動資產
                "2XXX" : ba[12],    #負債總計
                "21XX" : ba[13],    #流動負債合計
                "2570" : ba[14]     #遞延所得稅負債
            }
            income_statement = {
                "4000" : inc[0],    #營業收入合計
                "5000" : inc[1],    #營業成本合計
                "5900" : inc[2],    #營業毛利(毛損)
                "6000" : inc[3],    #營業費用合計
                "6900" : inc[4],    #營業利益(損失)
                "7000" : inc[5],    #營業外收入及支出合計
                "7900" : inc[6],    #繼續營業單位稅前(淨損)
                "7950" : inc[7],    #所得稅費用(利益)合計
                "8200" : inc[8],    #本期淨利(淨損)
                "9750" : inc[9]     #基本每股盈餘合計
            }
            money_flow = {
                "AAAA" : mo[0],     #營業活動之淨現金流入(流出)
                "BBBB" : mo[1],     #投資活動之淨現金流入(流出)
                "CCCC" : mo[2],     #籌資活動之淨現金流入(流出)
                "EEEE" : mo[3],     #本期現金及約當現金增加(減少)數
                "E00100" : mo[4],   #期初現金及約當現金餘額
                "E00200" : mo[5]    #期末現金及約當現金餘額
            }
            all_info = {
                "quarter" : ymqs[ym],                                #季別
                "balance_sheet_statement" : balance_sheet_statement,#資產負債表
                "income_statement" : income_statement,              #損益表
                "money_flow" : money_flow                           #現金流量表
            }
            ym += 1
            print(all_info)
            
            
if __name__ == "__main__":
    get_stock_info(2330)