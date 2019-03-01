from bs4 import BeautifulSoup
import requests,json
import hashlib
import re
import datetime
from datetime import date,timedelta
import calendar
import sqlite3
import os
import locale
import time  
locale.setlocale( locale.LC_ALL, "" )

sql = "INSERT INTO revence(日期,營收,月增率,去年同期,去年同期年增率,累計營收,累計營收年增率) \
       VALUES(?,?,?,?,?,?,?)" 
#check md5
class html_check:
    def __init__(self,ggg):
        self.html = requests.get("http://jsjustweb.jihsun.com.tw/z/zc/zch/zch_" + str(ggg)+".djhtm").text.encode('utf-8-sig')
        self.md5 = hashlib.md5(self.html).hexdigest()
        self.cur_path = os.path.dirname(__file__)
        self.test = str(ggg)  #test
    def check(self):
        if os.path.exists(self.cur_path+'\md5\old_md5.txt'):
            with open(self.cur_path+'\md5\old_md5.txt','r') as f:
                old_md5 =f.read()
        else:
            with open(self.cur_path+'\md5\old_md5.txt','w') as f:
                f.read(self.md5)
        return self.md5,old_md5
    def update(self):
        with open(self.cur_path+'\md5\old_md5.txt','w') as f:
           f.write(self.md5)
        return self.md5
    def qqw(self):       #test
        return self.test #test
#test
ff = html_check(2330)
print(ff.qqw()) #test




#將數字的小數點移除
def remove_dot(num):
    num_a = ''.join(str(num).split(','))
    return num_a

#個股營收
def getrevence(cur,k):
    r= requests.get("http://jsjustweb.jihsun.com.tw/z/zc/zch/zch_" + str(k)+".djhtm")  
    soup_all = BeautifulSoup(r.text,"html.parser")
    for tr in soup_all.select('table')[1].select('tr')[7:55]:
        td = tr.select('td')
        ret = (td[0].text,remove_dot(td[1].text),td[2].text,remove_dot(td[3].text),td[4].text
        ,remove_dot(td[5].text),td[6].text)
        cur.execute(sql,ret)

#財務比例
def fin(cur,k):
    r =requests.get('http://jsjustweb.jihsun.com.tw/z/zc/zcr/zcr0.djhtm?b=Q&a='+str(k))
    soup_all =BeautifulSoup()


#----------------開始執行--------------------#

#程式執行顯示畫面
def menu():
    os.system('cls')    #清除螢幕
    print('財務報表')
    print('-----------------------------')
#資料庫啟動
def go(k):
    cur_path = os.path.dirname(__file__)
    con = sqlite3.connect(cur_path+'\sqlite資料庫\/財務報表_'+ str(k) + '.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS revence(日期 text,\
                營收 int,月增率 int,去年同期 int,\
                去年同期年增率 int,累計營收 int,累計營收年增率 int)''')
    getrevence_html_md5 = html_check(k)
    if getrevence_html_md5.check()[0] != getrevence_html_md5.check()[1]:
        print(str(k)+'資料庫更新中')
        getrevence(cur,k)
        print(str(k)+'營收更新完成')
    else:
        print(str(k)+'資料庫為最新，不須更新')
    con.commit()
    con.close()

#while True:
#    menu()
#    choice = int(input('請輸入股票代碼:'))
#    print()
#    go(choice)





