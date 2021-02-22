import sys

import cv2
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi


class Start(QDialog):
    def __init__(self):
        super(Start, self).__init__()
        loadUi('gui.ui', self)
        self.image = None
        self.myButton.clicked.connect(self.loadClicked)

    @pyqtSlot()
    def loadClicked(self):
        self.loadImage('test.jpg')

    def loadImage(self, fname):
        self.image = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
        self.displayImage()

    def displayImage(self):
        qformat = QImage.Format_Indexed8

        if len(self.image.shape) == 3:
            if(self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(
            self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)

        img = img.rgbSwapped()
        self.imgLabel.setPixmap(QPixmap.fromImage(img))
        self.imgLabel.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Start()
    window.setWindowTitle('Show Image Form')
    window.show()
    sys.exit(app.exec_())
