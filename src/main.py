import sys 
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog , QApplication, QWidget, QStackedWidget
import sqlite3
import cart as cart

class Main (QDialog):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("./src/main.ui", self)
        self.loadData()
        self.allMenuButton.clicked.connect(self.loadData)
        self.tableWidget.clicked.connect(self.getMenu)
        self.addToCartButton.clicked.connect(self.addToCart)
        self.gtCartButton.clicked.connect(self.gtCart)

    def gtCart(self):
        self.umw = cart.Cart()
        self.umw.show()
        self.close()


    def loadData(self):
        db = sqlite3.connect("data.sqlite")
        cursor = db.cursor()
        sqlquery = "SELECT * FROM menu"
        result = cursor.execute(sqlquery).fetchall()
        row = 0
        self.tableWidget.setRowCount(len(result))
        for menu in result:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(menu[1]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(menu[2])))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(menu[3]))
            row += 1
    
    def getMenu(self):
        row = self.tableWidget.currentRow()
        rowMenuNama = self.tableWidget.item(row,0).text()
        rowMenuHarga = self.tableWidget.item(row,1).text()

        self.labelNama.setText(rowMenuNama)
        self.labelHarga.setText(rowMenuHarga)
        self.jumlahText.setText("0")

    def addToCart(self):
        row = self.tableWidget.currentRow()
        nama = self.tableWidget.item(row,0).text()
        harga =int( self.tableWidget.item(row,1).text())
        jumlah = int(self.jumlahText.text())
        total = harga*jumlah

        db = sqlite3.connect("data.sqlite")
        cursor = db.cursor()
        sqlquery = "SELECT * FROM keranjang WHERE nama = '"+nama+"'"
        result = cursor.execute(sqlquery).fetchall()
        if (len(result) == 0):
            sqlquery = "INSERT INTO keranjang (nama, kuantitas, harga_per_item, total) VALUES ('" + nama + "',"+str(jumlah)+","+str(harga)+","+str(total)+")"
        else :
            sqlquery = "UPDATE keranjang SET kuantitas = " + str(jumlah) + ", total = " + str(total)+" WHERE nama = '" + nama+"'"
        cursor.execute(sqlquery)
        db.commit()

app = QApplication(sys.argv)
window  = Main()
window.show()

try :
    sys.exit(app.exec_())
except:
    print("Exist")