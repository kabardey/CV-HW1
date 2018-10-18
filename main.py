import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QHBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QGroupBox, QAction, QFileDialog, qApp
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import cv2

##########################################

########################################

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()

        self.title = 'Histogram Equalization'
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 600

        self.inputLoaded = False
        self.targetLoaded = False

        self.initUI()


    def openInputImage(self):
        # This function is called when the user clicks File->Input Image.

        self.inputLoaded = True

        imagePath, _ = QFileDialog.getOpenFileName()
        inputImg = cv2.imread(imagePath)

        pixmap_label = self.qlabel1

        height, width, channel = inputImg.shape
        bytesPerLine = 3 * width
        qImg = QImage(inputImg.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(qImg)

        pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
        pixmap_label.setPixmap(pixmap)


    def openTargetImage(self):
        # This function is called when the user clicks File->Target Image.

        self.targetLoaded = True

        imagePath, _ = QFileDialog.getOpenFileName()
        inputImg = cv2.imread(imagePath)

        pixmap_label = self.qlabel2
        height, width, channel = inputImg.shape
        bytesPerLine = 3 * width
        qImg = QImage(inputImg.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(qImg)

        pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
        pixmap_label.setPixmap(pixmap)


    def initUI(self):
        # Write GUI initialization code

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)

        #****************add the labels for images*********************
        wid = QWidget(self)
        self.setCentralWidget(wid)

        b1 = QPushButton("Equalize Histogram")
        b1.clicked.connect(self.histogramButtonClicked)

        self.groupBox = QGroupBox()
        hBoxlayout = QHBoxLayout()

        self.qlabel1 = QLabel('Input', self)
        self.qlabel1.setStyleSheet("border: 1px inset grey; min-height: 200px; ")
        hBoxlayout.addWidget(self.qlabel1)

        self.qlabel2 = QLabel('Target', self)
        self.qlabel2.setStyleSheet("border: 1px inset grey; min-height: 200px; ")
        hBoxlayout.addWidget(self.qlabel2)

        self.qlabel3 = QLabel('Result', self)
        self.qlabel3.setStyleSheet("border: 1px inset grey; min-height: 200px; ")
        hBoxlayout.addWidget(self.qlabel3)

        self.groupBox.setLayout(hBoxlayout)

        vBox = QVBoxLayout()
        vBox.addWidget(b1)
        vBox.addWidget(self.groupBox)

        wid.setLayout(vBox)

        #****************menu bar***********
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        openAction = QAction('Open Input', self)
        openAction.triggered.connect(self.openInputImage)
        fileMenu.addAction(openAction)

        openAction2 = QAction('Target Input', self)
        openAction2.triggered.connect(self.openTargetImage)
        fileMenu.addAction(openAction2)

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAct)

        #------------------------------------
        self.show()


    def histogramButtonClicked(self):
        if not self.inputLoaded and not self.targetLoaded:
            # Error: "First load input and target images" in MessageBox
            QMessageBox.question(self, 'Error Message', "Please, load input image and target image", QMessageBox.Ok, QMessageBox.Ok)

        elif not self.inputLoaded:
            # Error: "Load input image" in MessageBox
            QMessageBox.question(self, 'Error Message', "Please, load input image", QMessageBox.Ok, QMessageBox.Ok)
        elif not self.targetLoaded:
            # Error: "Load target image" in MessageBox
            QMessageBox.question(self, 'Error Message', "Please, load target image", QMessageBox.Ok, QMessageBox.Ok)

    def calcHistogram(self, I):
        # Calculate histogram
        return NotImplementedError

class PlotCanvas(FigureCanvas):
    def __init__(self, hist, parent=None, width=5, height=4, dpi=100):
        return NotImplementedError
        # Init Canvas
        self.plotHistogram(hist)

    def plotHistogram(self, hist):
        return NotImplementedError
        # Plot histogram

        self.draw()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())