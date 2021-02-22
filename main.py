
import sys

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi


class Start(QDialog):
    def __init__(self):
        super(Start,self).__init__()
        loadUi('first.ui',self)

app = QApplication(sys.argv)
window = Start()
window.setWindowTitle("First GUI Window")
window.setGeometry(100,100,400,300)
window.show()
sys.exit(app.exec_())



