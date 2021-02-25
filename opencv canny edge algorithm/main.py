import sys

import cv2
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi


class Start(QDialog):
    def __init__(self):
        super(Start, self).__init__()
        loadUi('gui.ui', self)
        self.image = None
        self.button1.clicked.connect(self.loadClicked)
        self.button2.clicked.connect(self.saveClicked)
        self.button3.clicked.connect(self.cannyClicked)

    @pyqtSlot()
    def cannyClicked(self):
        gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY) if len(self.image.shape) >= 3 else self.image
        self.image = cv2.Canny(gray,100,200)
        self.displayImage(2)

    @pyqtSlot()
    def loadClicked(self):
        fname,filter = QFileDialog.getOpenFileName(self,'Open File','C:\\',"Image Files (*.jpg)")
        if fname:
            self.loadImage(fname)
        else:
            print('Invalid Image')

    @pyqtSlot()
    def saveClicked(self):
        fname, filter = QFileDialog.getSaveFileName(self, 'Save File', 'C:\\', "Image Files (*.jpg)")
        if fname:
            cv2.imwrite(fname, self.image)
        else:
            print('Error')

    def loadImage(self, fname):
        self.image = cv2.imread(fname, cv2.IMREAD_COLOR)
        self.displayImage(1)

    def displayImage(self,window = 1):
        qformat = QImage.Format_Indexed8

        if len(self.image.shape) == 3:
            if(self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(
            self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)

        img = img.rgbSwapped()
        if window == 1:
            self.imgLabel1.setPixmap(QPixmap.fromImage(img))
            self.imgLabel1.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        else:
            self.imgLabel2.setPixmap(QPixmap.fromImage(img))
            self.imgLabel2.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Start()
    window.setWindowTitle('Show Image Form')
    window.show()
    sys.exit(app.exec_())