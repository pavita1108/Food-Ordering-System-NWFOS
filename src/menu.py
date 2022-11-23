from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import  QPixmap
import sqlite3 
import random_id

class Menu (QDialog):
    def __init__(self):
        super(Menu, self).__init__()
        loadUi("./src/Menu.ui", self)
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
        pass

    
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
        self.jumlahText.setText("1")

    def addToCart(self):
        if self.jumlahText.text():
            row = self.tableWidget.currentRow()
            nama = self.tableWidget.item(row,1).text()
            harga =int( self.tableWidget.item(row,2).text())
            jumlah = int(self.jumlahText.text())
            
            if jumlah <= 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Jumlah Tidak Valid")
                msg.setInformativeText('Jumlah pembelian minimum adalah 1')
                msg.setWindowTitle("Jumlah Tidak Valid")
                msg.exec_()
                self.jumlahText.setText("1")
            
            else:
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
        else:
            msg2 = QMessageBox()
            msg2.setIcon(QMessageBox.Critical)
            msg2.setText("Anda Belum Memilih Menu")
            msg2.setInformativeText('Pililah menu terlebih dahulu sebelum melakukan penambahan ke keranjang')
            msg2.setWindowTitle("Menu Belum Dipilih")
            msg2.exec_()

            


