from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox
import sqlite3
import random_id

class Cart (QWidget):
    def __init__(self):
        super(Cart, self).__init__()
        loadUi("./src/cart.ui",self)
        self.loadData()
        self.tableWidget.clicked.connect(self.getMenu)
        self.plusButton.clicked.connect(self.plusItem)
        self.minButton.clicked.connect(self.minItem)
        self.resiButton.clicked.connect(self.printResi)
        self.back_2.clicked.connect(self.gtMenu)
        pass

    def printResi(self):
        if self.tableWidget.rowCount()<=0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Anda Belum Memesan")
            msg.setInformativeText('Keranjang anda masih kosong pesan sesuatu sebelum melakukan cetak resi')
            msg.setWindowTitle("KERANJANG KOSONG")
            msg.exec_()
        else:
            dlg = QMessageBox()
            dlg.setWindowTitle("Check Out?")
            dlg.setText("Checkout dan tampilkan resi")
            dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dlg.setIcon(QMessageBox.Question)
            button = dlg.exec()

            if button == QMessageBox.Yes:
                self.gtResi()

            
        
    def gtResi(self):
        pass


    def gtMenu(self):
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
        
    def getMenu(self):
        db = sqlite3.connect("data.sqlite")
        cursor = db.cursor()
        sqlquery = "SELECT * FROM keranjang WHERE id_keranjang = "+str(random_id.id_keranjang)
        result = cursor.execute(sqlquery).fetchall()
        if (len(result))==0:
            self.tableWidget.setRowCount(0)
            self.labelNama.setText("")
            self.labelHarga.setText("")
            self.labelTotal.setText("")
            self.kuantitasText.setText("")
        else:
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
        if self.labelNama.text() == "" :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Anda Tidak Bisa Melakukan Penambahan")
            msg.setInformativeText('Pilih menu untuk menambahkan jumlah item')
            msg.setWindowTitle("Anda Tidak Bisa Melakukan Penambahan")
            msg.exec_()
        else:
            row = self.tableWidget.currentRow()
            nama = self.tableWidget.item(row,0).text()
            if int(self.kuantitasText.text())>=0:
                kuantitas = int(self.kuantitasText.text()) +1
                harga =int(self.tableWidget.item(row,2).text())
                total = harga*kuantitas
                self.kuantitasText.setText(str(kuantitas))

                db = sqlite3.connect("data.sqlite")
                cursor = db.cursor()
                sqlquery = "UPDATE keranjang SET kuantitas = " + str(kuantitas) + ", total = " + str(total)+" WHERE nama = '"+nama+"' AND id_keranjang = " +str(random_id.id_keranjang)
                cursor.execute(sqlquery)
                db.commit()

                self.loadData()
                self.getMenu()
            else:
                db = sqlite3.connect("data.sqlite")
                cursor = db.cursor()
                sqlquery = "DELETE FROM keranjang WHERE nama = '"+nama+"' AND id_keranjang = " +str(random_id.id_keranjang)
                cursor.execute(sqlquery)
                db.commit()

                self.loadData()
                self.getMenu()

    def minItem (self):
        if self.labelNama.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Anda Tidak Bisa Melakukan Pengurangan")
            msg.setInformativeText('Pilih menu untuk mengurangi jumlah item')
            msg.setWindowTitle("Anda Tidak Bisa Melakukan Pengurangan")
            msg.exec_()
        else:
            row = self.tableWidget.currentRow()
            nama = self.tableWidget.item(row,0).text()
            if int(self.kuantitasText.text())>1:
                kuantitas = int(self.kuantitasText.text()) - 1
                harga =int(self.tableWidget.item(row,2).text())
                total = harga*kuantitas
                self.kuantitasText.setText(str(kuantitas))

                db = sqlite3.connect("data.sqlite")
                cursor = db.cursor()
                sqlquery = "UPDATE keranjang SET kuantitas = " + str(kuantitas) + ", total = " + str(total)+" WHERE nama = '"+nama+"' AND id_keranjang = " +str(random_id.id_keranjang)
                cursor.execute(sqlquery)
                db.commit()

                self.loadData()
                self.getMenu()
            else:
                db = sqlite3.connect("data.sqlite")
                cursor = db.cursor()
                sqlquery = "DELETE FROM keranjang WHERE nama = '"+nama+"' AND id_keranjang = " +str(random_id.id_keranjang)
                cursor.execute(sqlquery)
                db.commit()

                self.loadData()
                self.getMenu()

    


        