import sqlite3
import random

def idGenerator ():
        global id_keranjang
        db = sqlite3.connect("data.sqlite")
        cursor = db.cursor()
        id = random.randint(0, 10000)
        sqlquery = "SELECT * FROM keranjang WHERE id_keranjang = "+str(id)
        result = cursor.execute(sqlquery).fetchall()
        while (len(result) > 0) :
            id = random.randint(0, 10000)
            sqlquery = "SELECT * FROM keranjang WHERE id_keranjang = "+str(id)
            result = cursor.execute(sqlquery).fetchall()
        id_keranjang = id