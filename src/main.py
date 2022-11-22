import sys 
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog , QApplication, QWidget, QStackedWidget, QLabel
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui import QIcon, QPixmap
import sqlite3
import cart 
import random_id

class Main (QDialog):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("./src/main.ui", self)
        db = sqlite3.connect("data.sqlite")
        cursor = db.cursor()
        sqlquery = "SELECT * FROM menu"
        result = cursor.execute(sqlquery).fetchall()
        self.tableWidget.setRowCount(len(result))
        completerList = []
        for row in range(len(result)):
            completerList.append(str(result[row][1]))
            for column in range(4):
                column_data = result[row][column]
                if (column == 0) :
                    item = self.getImageLabel(column_data)
                    self.tableWidget.setCellWidget(row,column,item)
                else : 
                    item = QtWidgets.QTableWidgetItem(str(result[row][column]))
                    self.tableWidget.setItem(row, column, item)

        self.searchText.textChanged.connect(self.filtermenu)
        self.allMenuButton.clicked.connect(self.searchText.clear)
        self.tableWidget.clicked.connect(self.getMenu)
        self.addToCartButton.clicked.connect(self.addToCart)
        self.gtCartButton.clicked.connect(self.gtCart)

        #search bar auto completer
        self.completer = QtWidgets.QCompleter(completerList)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchText.setCompleter(self.completer)

    def getImageLabel(self,image):
        imageLabel = QtWidgets.QLabel(self)
        imageLabel.setScaledContents(True)
        pixmap = QPixmap()
        pixmap.loadFromData(image,'jpg')
        imageLabel.setPixmap(pixmap)
        return imageLabel

    def gtCart(self):
        self.umw = cart.Cart()
        self.umw.show()
        self.close()

    
    def filtermenu (self, filter_text):
        for i in range(self.tableWidget.rowCount()):
            for j in range (1, self.tableWidget.columnCount()):
                item = self.tableWidget.item(i, j)
                match = filter_text.lower() not in item.text().lower()
                self.tableWidget.setRowHidden(i, match)
                if not match:
                    break
    
    def getMenu(self):
        row = self.tableWidget.currentRow()
        rowMenuNama = self.tableWidget.item(row,1).text()
        rowMenuHarga = self.tableWidget.item(row,2).text()

        self.labelNama.setText(rowMenuNama)
        self.labelHarga.setText(rowMenuHarga)
        self.jumlahText.setText("0")

    def addToCart(self):
        row = self.tableWidget.currentRow()
        nama = self.tableWidget.item(row,1).text()
        harga =int( self.tableWidget.item(row,2).text())
        jumlah = int(self.jumlahText.text())
        total = harga*jumlah

        db = sqlite3.connect("data.sqlite")
        cursor = db.cursor()
        sqlquery = "SELECT * FROM keranjang WHERE nama = '"+nama+"' AND id_keranjang = " +str(random_id.id_keranjang)
        result = cursor.execute(sqlquery).fetchall()
        if (len(result) == 0):
            sqlquery = "INSERT INTO keranjang (id_keranjang, nama, kuantitas, harga_per_item, total) VALUES ( "+str(random_id.id_keranjang)+",'" + nama + "',"+str(jumlah)+","+str(harga)+","+str(total)+")"
        else :
            sqlquery = "UPDATE keranjang SET kuantitas = " + str(jumlah) + ", total = " + str(total)+" WHERE nama = '"+nama+"' AND id_keranjang = " +str(random_id.id_keranjang)
        cursor.execute(sqlquery)
        db.commit()
            


random_id.idGenerator()
app = QApplication(sys.argv)
window  = Main()
window.show()

try :
    sys.exit(app.exec_())
except:
    print("Exist")