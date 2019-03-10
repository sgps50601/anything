# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import sqlite3



cur_path = os.path.dirname(__file__)
con = sqlite3.connect(cur_path+'\sqlite資料庫\/麥克連資料庫.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS stock(日期 text,\
                加權指數 int,加權漲跌 int,成交量_億 int,\
                外資股買賣超_億 int,台幣匯率 int,外資期未平倉口數 int,\
                未平倉與結算日相比 int,外資選擇權未平倉_買 int,外資選擇權未平倉_賣 int,\
                PC_ratio int,期前十大留倉口數_當月 int,期前十大留倉口數_所有 int,\
                期前十大未來看法 int,散戶看多 int,散戶看空 int,散戶多空比 int)''')

cur.execute("SELECT 日期,加權指數,外資期未平倉口數 FROM stock ")
data = cur.fetchall()
for row in data:
    print(row[0],row[1],row[2])

con.commit()
con.close()
