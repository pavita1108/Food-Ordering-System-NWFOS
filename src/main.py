import sys 
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog , QApplication, QWidget, QStackedWidget, QLabel
from PyQt5.QtCore import Qt,QSize
# from PyQt5.QtCore import * 
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
         #metadat: [('M1', 'Bacon, Egg & Cheese Biscuit', 20000, "The McDonald's Bacon, Egg & Cheese Biscuit breakfast sandwich features a warm, buttermilk biscuit brushe
# d with real butter, thick cut Applewood smoked bacon, a fluffy folded egg, and a slice of melty American cheese."), ('M2', 'Egg McMuffin', 30000, 'Our 
# Egg McMuffin® breakfast sandwich is an excellent source of protein and oh so delicious. We place a freshly cracked Grade A egg on a toasted English Muf
# fin topped with real butter and add lean Canadian bacon and melty American cheese.'), ('M3', 'Sausage McMuffin', 25000, "McDonald's Sausage McMuffin® r
# ecipe features a warm, freshly toasted English muffin, topped with a savory hot sausage patty and a slice of melty American cheese")]
        # self.tableWidget.setRowCount(len(result))
        completerList = []
        # for row in range(len(result)):
        #     completerList.append(str(result[row][1]))
        #     for column in range(3):
        #         # print(result[row][column+1])
        #         item = QtWidgets.QTableWidgetItem(str(result[row][column+1]))
        #         label = QLabel()
        #         # pixmap = Qpixmap(column+1,'.jpeg')
        #         self.tableWidget.setItem(row, column, item)
        for row_number,row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            completerList.append(str(result[row_number][1]))
            for column_number, column_data in enumerate(row_data):
                it = QtWidgets.QTableWidgetItem()
                if(column_number == 0):
                    # print(column_data)
                    # item = self.getImageLabel(column_data)
                    imagelabel = QDialog.QLabel(self.centralwidget)
                    imagelabel.setText("")
                    imagelabel.setScaledContents(True)
                    pixmap = QPixmap()
                    pixmap.loadFromData(column_data)
                    item = imagelabel.setPixmap(pixmap)
                    self.tablewidget.setCellWidget(rown_number, column_number, item)
                    # it.setIcon(QIcon(pixmap.scaled(500, 500)))
                    # size = QSize(10, 10)
                    # it.setIconSize(size)
                else:
                    item = str(column_data)
                    it.setText(str(item))
                    self.tableWidget.setItem(row_number,column_number,it)
                
        self.searchText.textChanged.connect(self.filtermenu)
        self.allMenuButton.clicked.connect(self.searchText.clear)
        self.tableWidget.clicked.connect(self.getMenu)
        self.addToCartButton.clicked.connect(self.addToCart)
        self.gtCartButton.clicked.connect(self.gtCart)

        #search bar auto completer
        self.completer = QtWidgets.QCompleter(completerList)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchText.setCompleter(self.completer)

    # def getImageLabel(image):
    #     pixmap = QPixmap()
    #     pixmap.loadFromData(image,'jpg')
    #     imageLabel.setPixmap(pixmap)
    #     return imageLabel

    def gtCart(self):
        self.umw = cart.Cart()
        self.umw.show()
        self.close()

    
    def filtermenu (self, filter_text):
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
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