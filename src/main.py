import sys
from menu import Menu
from cart import Cart
from resi import Resi
import random_id
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

random_id.idGenerator()
app = QApplication(sys.argv)

class Smenu(Menu):
    def gtCart(self):
        cartscreen = Scart()
        screen.addWidget(cartscreen)
        screen.setCurrentIndex(screen.count()-1)


class Scart(Cart):
    def gtMenu(self):
        screen.setCurrentWidget(menuscreen)

    def gtResi(self):
        resiscreen = Resi()
        screen.addWidget(resiscreen)
        screen.setCurrentIndex(screen.count()-1)
  

screen = QtWidgets.QStackedWidget()
menuscreen = Smenu()
screen.addWidget(menuscreen)
screen.setCurrentWidget(menuscreen)
screen.setFixedHeight(720)
screen.setFixedWidth(1280)
screen.show()
screen.setWindowTitle("NWFOS")

try :
    sys.exit(app.exec_())
except:
    print("Exist")