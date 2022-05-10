import os
import sqlite3

conn = sqlite3.connect("test.db")
cur = conn.cursor()

file = open("question.txt","a")
cur.execute("select name, shares, price from portfolio where account=12345")
file.write((str((format("NAME", "<20s"), format("SHARES", "^15s"), format("PRICE", ">12s")))))
file.write((str((format("-----------", "<20s"), format("------------", "^15s"), format("--------", ">12s")))))

for name, shares, price in cur:
     print(format(name, "<20s"), format(shares, "^15d"), format(price, ">10.2f"))

