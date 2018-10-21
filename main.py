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


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()

        self.title = 'Histogram Matching'
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

        # ******** place image into qlabel object *********************
        imagePath, _ = QFileDialog.getOpenFileName()
        self.inputImg = cv2.imread(imagePath)

        pixmap_label = self.qlabel1

        height, width, channel = self.inputImg.shape
        bytesPerLine = 3 * width
        qImg = QImage(self.inputImg.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(qImg)

        pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
        pixmap_label.setPixmap(pixmap)
        # **************************************************************

        # **************** create histogram ***************************
        # allocate for histogram
        self.hist1 = np.zeros(([256, channel]))

        # create the histogram
        for g in range(256):
            for b in range(3):  # through channels
                self.hist1[g, b] = np.sum(np.sum(self.inputImg[:, :, b] == g, 0), 0)
        # **************************************************************

        # ************* add histogram to hbox object ******************
        self.myfig = PlotCanvas(self, width=5, height=4, dpi=100, histr=self.hist1, title="Input Image")
        self.hBoxlayout2.addWidget(self.myfig)

    def openTargetImage(self):
        # This function is called when the user clicks File->Target Image.

        self.targetLoaded = True

        # ******** place image into qlabel object *********************
        imagePath, _ = QFileDialog.getOpenFileName()
        self.targetImg = cv2.imread(imagePath)

        pixmap_label = self.qlabel2

        height, width, channel = self.targetImg.shape
        bytesPerLine = 3 * width
        qImg = QImage(self.targetImg.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(qImg)

        pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
        pixmap_label.setPixmap(pixmap)
        #**************************************************************

        # **************** create histogram ***************************
        # allocate for histogram
        self.hist2 = np.zeros(([256, channel]))

        # create the histogram
        for g in range(256):
            for b in range(3):  # through channels
                self.hist2[g, b] = np.sum(np.sum(self.targetImg[:, :, b] == g, 0), 0)

        #**************************************************************

        # ************* add histogram to hbox object ******************
        self.myfig = PlotCanvas(self, width=5, height=4, dpi=100, histr=self.hist2, title="Target Image")
        self.hBoxlayout2.addWidget(self.myfig)

    def initUI(self):
        # Write GUI initialization code

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)

        #****************add the labels for images*********************
        wid = QWidget(self)
        self.setCentralWidget(wid)

        b1 = QPushButton("Match Histogram")
        b1.clicked.connect(self.histogramButtonClicked)

        self.groupBox = QGroupBox()
        self.hBoxlayout = QHBoxLayout()

        self.qlabel1 = QLabel('Input', self)
        self.qlabel1.setStyleSheet("border: 1px inset grey; min-height: 200px; ")
        self.qlabel1.setAlignment(Qt.AlignCenter)
        self.hBoxlayout.addWidget(self.qlabel1)

        self.qlabel2 = QLabel('Target', self)
        self.qlabel2.setStyleSheet("border: 1px inset grey; min-height: 200px; ")
        self.qlabel2.setAlignment(Qt.AlignCenter)
        self.hBoxlayout.addWidget(self.qlabel2)

        self.qlabel3 = QLabel('Result', self)
        self.qlabel3.setStyleSheet("border: 1px inset grey; min-height: 200px; ")
        self.qlabel3.setAlignment(Qt.AlignCenter)
        self.hBoxlayout.addWidget(self.qlabel3)

        self.groupBox.setLayout(self.hBoxlayout)

        #************add histogram layers*************
        self.groupBox2 = QGroupBox()
        self.hBoxlayout2 = QHBoxLayout()
        self.groupBox2.setLayout(self.hBoxlayout2)

        vBox = QVBoxLayout()
        vBox.addWidget(b1)
        vBox.addWidget(self.groupBox)
        vBox.addWidget(self.groupBox2)

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
        else:
            self.calcHistogram()

    def calcHistogram(self):
        # Calculate matching histogram

        input_height, input_width, input_channel = self.inputImg.shape
        target_height, target_width, target_channel = self.targetImg.shape

        # allocate for probability density function(pdf)
        pdf1 = np.zeros(([256, input_channel]))
        pdf2 = np.zeros(([256, target_channel]))

        # create pdf for input image
        for g in range(256):
            for b in range(3):  # through channels
                pdf1[g, b] = ((self.hist1[g, b]) / (input_height * input_width))    # input
                pdf2[g, b] = ((self.hist2[g, b]) / (target_height * target_width))  # target

        # create cdf
        cdf1 = np.zeros(([256, input_channel]))
        cdf2 = np.zeros(([256, target_channel]))

        cdf1[:, 0] = np.cumsum(pdf1[:, 0])
        cdf1[:, 1] = np.cumsum(pdf1[:, 1])
        cdf1[:, 2] = np.cumsum(pdf1[:, 2])

        cdf2[:, 0] = np.cumsum(pdf2[:, 0])
        cdf2[:, 1] = np.cumsum(pdf2[:, 1])
        cdf2[:, 2] = np.cumsum(pdf2[:, 2])

        # create look up table(LUT)
        LUT_R = np.zeros((256, 1), dtype=np.uint8)
        LUT_G = np.zeros((256, 1), dtype=np.uint8)
        LUT_B = np.zeros((256, 1), dtype=np.uint8)

        for i in range(255):
            for j in range(255):
                if(cdf1[i, 0] < cdf2[j, 0]):
                    LUT_B[i] = j
                    break;

        for i in range(255):
            for j in range(255):
                if(cdf1[i, 1] < cdf2[j, 1]):
                    LUT_G[i] = j
                    break;

        for i in range(255):
            for j in range(255):
                if(cdf1[i, 2] < cdf2[j, 2]):
                    LUT_R[i] = j
                    break;


        self.result_image = np.zeros((target_height, target_width, 3), dtype=np.uint8)

        #look look up table and match the histogram
        for height in range(target_height):
            for width in range(target_width):
                pixel1 = self.inputImg[height, width, 0]
                pixel2 = self.inputImg[height, width, 1]
                pixel3 = self.inputImg[height, width, 2]

                self.result_image[height, width, 0] = LUT_B[pixel1]
                self.result_image[height, width, 1] = LUT_G[pixel2]
                self.result_image[height, width, 2] = LUT_R[pixel3]


        #place the result image into box
        pixmap_label = self.qlabel3

        bytesPerLine = 3 * target_width
        qImg = QImage(self.result_image.data, target_width, target_height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(qImg)

        pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
        pixmap_label.setPixmap(pixmap)

        # ******allocate for histogram**********
        self.hist3 = np.zeros(([256, target_channel]))

        # create the histogram
        for g in range(256):
            for b in range(3):  # through channels
                self.hist3[g, b] = np.sum(np.sum(self.result_image[:, :, b] == g, 0), 0)

        self.myfig = PlotCanvas(self, width=5, height=4, dpi=100, histr=self.hist3, title="Result Image")
        self.hBoxlayout2.addWidget(self.myfig)


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, histr=0, title=""):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes1 = fig.add_subplot(311)
        self.axes2 = fig.add_subplot(312)
        self.axes3 = fig.add_subplot(313)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plotHistogram(histr, title)


    def plotHistogram(self, histr, title):
        ######## create histogram ########

        ax1 = self.axes1
        ax1.bar(range(0, 256), histr[:, 0], color=[0, 0, 1])
        ax1.set_title(title)

        ax2 = self.axes2
        ax2.bar(range(0, 256), histr[:, 1], color=[0, 1, 0])

        ax3 = self.axes3
        ax3.bar(range(0, 256), histr[:, 2], color=[1, 0, 0])

        self.draw()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())