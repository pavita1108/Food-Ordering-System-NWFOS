from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
import sqlite3
import random_id

class Resi (QWidget):
    def __init__(self):
        super(Resi, self).__init__()
        loadUi("./src/resi.ui",self)
        self.loadData()
        self.cetakResi()
        pass

    def loadData(self):
        db = sqlite3.connect("data.sqlite")
        cursor = db.cursor()
        sqlquery = "SELECT * FROM keranjang WHERE id_keranjang = "+str(random_id.id_keranjang)
        result = cursor.execute(sqlquery).fetchall()
        row = 0
        self.tableWidget.setRowCount(len(result))
        for menu in result:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(menu[1]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(menu[2])))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(menu[3])))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(menu[4])))
            row += 1

    def hitungTotal (self) :
        harga = 0
        db = sqlite3.connect("data.sqlite")
        cursor = db.cursor()
        sqlquery = "SELECT * FROM keranjang WHERE id_keranjang = "+str(random_id.id_keranjang)
        result = cursor.execute(sqlquery).fetchall()
        row = 0
        self.tableWidget.setRowCount(len(result))
        for menu in result:
            harga = harga + menu[4]
            row += 1
        
        return harga
    
    def cetakResi (self):
        harga = self.hitungTotal()
        self.labelTotal.setText(str(harga))
        self.labelID.setText(str(random_id.id_keranjang))
        db = sqlite3.connect("data.sqlite")
        cursor = db.cursor()
        sqlquery = "INSERT INTO resi (id_keranjang, total) VALUES ( " + str(random_id.id_keranjang) + ", " +str(harga)+")"
        cursor.execute(sqlquery)
        db.commit()

    