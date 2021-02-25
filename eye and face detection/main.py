import sys

import cv2
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi


class Start(QDialog):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    def __init__(self):
        super(Start, self).__init__()
        loadUi('gui.ui', self)
        self.image = None
        self.processedImage = None
        self.button1.clicked.connect(self.loadClicked)
        self.button2.clicked.connect(self.saveClicked)
        self.button3.clicked.connect(self.detectClicked)

    @pyqtSlot()
    def cannyDisplay(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) if len(
            self.image.shape) >= 3 else self.image
        self.processedImage = cv2.Canny(
            gray, self.hSlider.value(), self.hSlider.value()*3)
        self.displayImage(2)

    @pyqtSlot()
    def detectClicked(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) if len(
            self.image.shape) >= 3 else self.image
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        for(x, y, w, h) in faces:
            if self.c1.isChecked():
                cv2.rectangle(self.processedImage, (x, y),
                              (x+w, y+h), (255, 0, 0), 2)
            else:
                self.processedImage = self.image.copy()
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = self.processedImage[y:y+h, x:x+w]
            if self.c2.isChecked():
                eyes = self.eye_cascade.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey),
                                  (ex+ew, ey+eh), (0, 255, 0), 2)
            else:
                self.processedImage[y:y+h, x:x +
                                    w] = self.image[y:y+h, x:x+w].copy()

        self.displayImage(2)

    @pyqtSlot()
    def loadClicked(self):
        fname, filter = QFileDialog.getOpenFileName(
            self, 'Open File', 'C:\\', "Image Files (*.jpg)")
        if fname:
            self.loadImage(fname)
        else:
            print('Invalid Image')

    @pyqtSlot()
    def saveClicked(self):
        fname, filter = QFileDialog.getSaveFileName(
            self, 'Save File', 'C:\\', "Image Files (*.jpg)")
        if fname:
            cv2.imwrite(fname, self.processedImage)
        else:
            print('Error')

    def loadImage(self, fname):
        self.image = cv2.imread(fname, cv2.IMREAD_COLOR)
        self.processedImage = self.image.copy()
        self.displayImage(1)

    def displayImage(self, window=1):
        qformat = QImage.Format_Indexed8

        if len(self.processedImage.shape) == 3:  # rows[0],cols[1],channels[2]
            if(self.processedImage.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(self.processedImage,
                     self.processedImage.shape[1], self.processedImage.shape[0], self.processedImage.strides[0], qformat)
        #BGR > RGB
        img = img.rgbSwapped()
        if window == 1:
            self.imgLabel1.setPixmap(QPixmap.fromImage(img))
            self.imgLabel1.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        if window == 2:
            self.imgLabel2.setPixmap(QPixmap.fromImage(img))
            self.imgLabel2.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Start()
    window.setWindowTitle('Image Processing Form')
    window.show()
    sys.exit(app.exec_())
