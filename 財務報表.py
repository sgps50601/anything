import calendar
import datetime
import hashlib
import json
import locale
import os
import re
import sqlite3
import time
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup

locale.setlocale( locale.LC_ALL, "" )

k ='2330'
input_infomation = {
                    '損益表_季':[k, "http://jsjustweb.jihsun.com.tw/z/zc/zcq/zcq_",["期別","營業收入淨額","營業成本"]],
                    '財務狀況表_季':[k,"http://jsjustweb.jihsun.com.tw/z/zc/zcp/zcpa/zcpa_",["期別","現金及約當現金"]],
                    '現金流量表_季':[k,"http://jsjustweb.jihsun.com.tw/z/zc/zc3/zc3_",["期別","折舊－CFO","利息收入－CFO"]]
                    }
input_infomation2 = {
                    '財務比例表_季':[k, "http://jsjustweb.jihsun.com.tw/z/zc/zcr/zcr_",["期別","營業毛利率","淨值/資產","營收成長率","應收帳款週轉次","流動比率","現金流量比率"]],
                    }

#個股營收sql
sql = "INSERT INTO Revence(日期,營收,月增率,去年同期,去年同期年增率,累計營收,累計營收年增率) \
       VALUES(?,?,?,?,?,?,?)"

#未來寫程式要把導入變數放入def 而不是放在__init__，避免未來不斷定義
#檢測網頁是否更新md5
class check_html():
    def __init__(self,title,k,url):
        self.title = title
        self.html = requests.get(url + str(k)).text.encode('utf-8-sig')
        self.md5 = hashlib.md5(self.html).hexdigest()
        self.old_md5 = ""
        self.cur_path = os.path.dirname(__file__)
    def check_md5(self):
        print(self.title + "的md5碼=" + self.md5)
        if os.path.exists(cur_path+'\md5\old_md5_' + k + self.title + '.txt'): #如果有舊的md5，讀取存入變數old_md5
            with open(cur_path+'\md5\old_md5_' + k + self.title + '.txt','r') as f:
                self.old_md5 =f.read()
        with open(cur_path+'\md5\old_md5_' + k + self.title + '.txt','w') as f:
            f.write(self.md5)
        return self.old_md5,self.md5



#建立財報分析atr1類別
class atr1(check_html):
    def __init__(self,name):
        self.uname = name
        self.num_b = []   #串列數字移除小數點用
        self.report1_list = [] #網站報表report1、2表的種類
        self.report2_list = [] 
        self.report1_list_r = []#Report1、2方法會把input_infomation字典中要分析的種類expend進去此串列，
        self.report2_list_r = []

    #將'字串'數字的小數點移除
    def __remove_dot(self,num):
        num_a = ''.join(str(num).split(','))
        return num_a
    #將'串列'數字的小數點移除
    def __remove_dot2(self,num):
        self.num_b.clear()
        for num_a in num:
            num_a = ''.join(str(num_a).split(','))
            self.num_b.append(num_a)
        return self.num_b
    #個股營收
    def Revence(self,cur,k):
        r= requests.get("http://jsjustweb.jihsun.com.tw/z/zc/zch/zch_" + str(k)+".djhtm")  
        soup_all = BeautifulSoup(r.text,"html.parser")
        for tr in soup_all.select('table')[1].select('tr')[7:55]:
            td = tr.select('td')
            ret = (td[0].text,self.__remove_dot(td[1].text),td[2].text,self.__remove_dot(td[3].text),td[4].text
            ,self.__remove_dot(td[5].text),td[6].text)
            cur.execute(sql,ret)
    #損益表、財務狀況表、現金流量表
    def Report1(self,cur,title,k,web,input_list):
            self.report1_list.clear()
            self.report1_list_r.clear()
            self.report1_list_r.extend(input_list)
            r = requests.get(web + str(k)+".djhtm")
            soup_all = BeautifulSoup(r.text,"html.parser")
            for tr in soup_all.select('tr')[2]:  #篩選表格，全部資料放進td這個串列(list)
                td = tr.select('td')
            for td_r in td:  #取出td串列，用text去除雜項再append放入td_rr字串
                td_r = td_r.text
                td_r = td_r.lstrip()
                self.report1_list.append(td_r)
            print(self.report1_list[1:10])  #篩選出損益表種類(ex營業收入毛額、營業費用...)
            print("--------------------------------------------------------------")            
            print("X檢查鍵入種類是否在「" + title + "」報表中X")
            for want in self.report1_list_r:
                if want in self.report1_list[1::9]:
                    print(want,"ok")
                    report1_number = self.report1_list.index(want)
                    ret = self.report1_list[report1_number : report1_number + 9] #ret=取出一列串列 ex[營收,1254,4521,...]
                    ret2 = self.__remove_dot2(ret)                #ret2=放入__remove_dot2方法移除小數點
                    cur.execute("INSERT INTO Report1 values('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(ret2[0],ret2[1],ret2[2],ret2[3],ret2[4],ret2[5],ret2[6],ret2[7],ret2[8]))                 
                else:
                    print(want,"Error(種類不在「"+ title + "」中)")
            m =re.match(r'[\S]+',self.report1_list[0])
            print(m.group()) 
    #財務比例表
    def Report2(self,cur,title,k,web,input_list):
            self.report2_list.clear()
            self.report2_list_r.clear()
            self.report2_list_r.extend(input_list)
            r = requests.get(web + str(k)+".djhtm") 
            soup_all = BeautifulSoup(r.text,"html.parser")
            for tr in soup_all.select('tr')[2]:  #篩選表格，全部資料放進td這個串列(list)
                td = tr.select('td')
            for td_r in td:  #取出td串列，用text去除雜項再append放入td_rr字串
                self.report2_list.append(td_r.text)

            #print(self.report2_list) 
            print("--------------------------------------------------------------")            
            print("X檢查鍵入種類是否在「" + title + "」報表中X")
            #比例表並非跟上面損益表依樣每9個循環，故要分別拆開，在合併
            a = set(self.report2_list[2:127:9])  #比例表-獲利能力指標
            b = set(self.report2_list[129:215:9]) #比例表-每股比率指標
            c = set(self.report2_list[238:374:9]) #比例表-成長率指標
            d = set(self.report2_list[374:491:9]) #比例表-經營能力指標
            e = set(self.report2_list[492:600:9]) #比例表-償債能力指標
            #for want1,want2,want3,want4,want5 in zip(a,b,c,d,e):
            #    print(want5)
            for want in self.report2_list_r:
                if (want in a) or (want in b) or (want in c) or (want in d) or (want in e):
                    print(want + 'ok')
                    report2_number = self.report2_list.index(want)
                    ret = self.report2_list[report2_number : report2_number + 9] #ret=取出一列串列 ex[營收,1254,4521,...]
                    ret2 = self.__remove_dot2(ret)
                    cur.execute("INSERT INTO Report2 values('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(ret2[0],ret2[1],ret2[2],ret2[3],ret2[4],ret2[5],ret2[6],ret2[7],ret2[8])) 
                else:
                    print(want + 'nook')   
cur_path = os.path.dirname(__file__)
con = sqlite3.connect(cur_path+'\sqlite資料庫\/財務報表_'+ str(k) + '.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Revence(日期 text,\
            營收 int,月增率 int,去年同期 int,\
            去年同期年增率 int,累計營收 int,累計營收年增率 int)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Report1(種類 text,\
            日期1 int,日期2 int,日期3 int,日期4 int,日期5 int,日期6 int,日期7 int,日期8 int)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Report2(種類 text,\
            日期1 int,日期2 int,日期3 int,日期4 int,日期5 int,日期6 int,日期7 int,日期8 int)''')

#定義財報分析類別為f1
f1 = atr1('基礎財報分析')

f2 = check_html("每月營收",k,"http://jsjustweb.jihsun.com.tw/z/zc/zch/zch_")
if f2.check_md5()[0] != f2.check_md5()[0]:
    print("md5不一樣，網站已更新")
    f1.Revence(cur,k)
else:
    print("md5碼一樣，不用更新")

for title,contents in input_infomation.items(): 
     f3 = check_html(title,contents[0],contents[1])
     if f3.check_md5()[0] != f3.check_md5()[0]:
          print("md5不一樣，網站已更新")
          f1.Report1(cur,title,contents[0],contents[1],contents[2])
     else:
          print("md5碼一樣，不用更新")
    
#for title,contents in input_infomation2.items():
#    f1.Report2(cur,title,contents[0],contents[1],contents[2])
con.commit()
con.close()

#md5測試