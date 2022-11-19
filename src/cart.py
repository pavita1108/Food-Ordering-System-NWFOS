import sys 
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog , QApplication, QWidget, QStackedWidget
import sqlite3

class Cart (QWidget):
    def __init__(self):
        super(Cart, self).__init__()
        loadUi("./src/cart.ui",self)
        self.loadData()
        self.tableWidget.clicked.connect(self.getMenu)
        self.plusButton.clicked.connect(self.plusItem)
        self.minButton.clicked.connect(self.minItem)
        pass
    
    def loadData(self):
        db = sqlite3.connect("data.sqlite")
        cursor = db.cursor()
        sqlquery = "SELECT * FROM keranjang"
        result = cursor.execute(sqlquery).fetchall()
        row = 0
        self.tableWidget.setRowCount(len(result))
        for menu in result:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(menu[0]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(menu[1])))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(menu[2])))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(menu[3])))
            row += 1
        
    def getMenu(self):
        row = self.tableWidget.currentRow()
        rowNama = self.tableWidget.item(row,0).text()
        rowKuantitas = self.tableWidget.item(row,1).text()
        rowHarga = self.tableWidget.item(row,2).text()
        rowTotal = self.tableWidget.item(row,3).text()

        self.labelNama.setText(rowNama)
        self.labelHarga.setText(rowHarga)
        self.labelTotal.setText(rowTotal)
        self.kuantitasText.setText(rowKuantitas)
    
    def plusItem (self):
        row = self.tableWidget.currentRow()
        nama = self.tableWidget.item(row,0).text()
        kuantitas = int(self.kuantitasText.text()) +1
        harga =int(self.tableWidget.item(row,2).text())
        total = harga*kuantitas
        self.kuantitasText.setText(str(kuantitas))

        db = sqlite3.connect("data.sqlite")
        cursor = db.cursor()
        sqlquery = "UPDATE keranjang SET kuantitas = " + str(kuantitas) + ", total = " + str(total)+" WHERE nama = '" + nama+"'"
        cursor.execute(sqlquery)
        db.commit()

        self.loadData()
        self.getMenu()

    def minItem (self):
        row = self.tableWidget.currentRow()
        nama = self.tableWidget.item(row,0).text()
        kuantitas = int(self.kuantitasText.text()) - 1
        harga =int(self.tableWidget.item(row,2).text())
        total = harga*kuantitas
        self.kuantitasText.setText(str(kuantitas))

        db = sqlite3.connect("data.sqlite")
        cursor = db.cursor()
        sqlquery = "UPDATE keranjang SET kuantitas = " + str(kuantitas) + ", total = " + str(total)+" WHERE nama = '" + nama+"'"
        cursor.execute(sqlquery)
        db.commit()

        self.loadData()
        self.getMenu()


        