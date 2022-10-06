from django.db import connection
import pymysql

con = pymysql.connect(host='localhost', user='root', password='',db='kuinvest', charset='utf8') # 한글처리 (charset = 'utf8')
cursor = con.cursor()
session = 'test'
input_fav_buy = 'HDC현대산업개발보통주'
sql1 = "select price, cnt from kuproject_stock_fav where user_id = '" + session + "' and name = '" + input_fav_buy + "';"

cursor.execute(sql1)
data = cursor.fetchall()


oprice = data[0][0]
ocnt = data[0][1]
price = 8000
cnt = 5
if oprice == 0:
    tprice = price
    tcnt = cnt
else:
    tprice = (oprice * ocnt + price * cnt) // (ocnt + cnt)
    tcnt = ocnt + cnt

print(tprice, tcnt)
sql2 = "update kuproject_stock_fav set price = " + str(tprice) + ", cnt = " + str(tcnt) + " where user_id = '" + session + "' and name = '" + input_fav_buy + "';"
cursor.execute(sql2)
con.commit()
con.close()