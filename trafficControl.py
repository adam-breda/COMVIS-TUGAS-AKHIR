# import the necessary packages
import numpy as np
# import imutils
import time
from scipy import spatial
import cv2
import os
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QAction, QMainWindow, QSlider, QPushButton, QToolTip, QApplication
import torch


class Ui_MainWindow(QMainWindow):
    video_one_path = ""
    video_two_path = ""
    video_three_path = ""

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('Traffic.ui', self)
        self.btnSelectVideoOne = self.findChild(QtWidgets.QPushButton, 'select_video_one')
        self.btnSelectVideoOne.clicked.connect(self.GetFileFirstpath)

        self.btnSelectVideoTwo = self.findChild(QtWidgets.QPushButton, 'select_video_two')
        self.btnSelectVideoTwo.clicked.connect(self.GetFileSecondpath) 

        self.btnSelectVideoThree = self.findChild(QtWidgets.QPushButton, 'select_video_three')
        self.btnSelectVideoThree.clicked.connect(self.GetFileThirdpath) 

        self.btnFlipHorizontal = self.findChild(QtWidgets.QPushButton, 'btn_run_detection')
        self.btnFlipHorizontal.clicked.connect(self.Detect)

        self.txtVideoOne = self.findChild(QtWidgets.QPlainTextEdit, 'plainTextEdit_3')
        self.txtVideoTwo = self.findChild(QtWidgets.QPlainTextEdit, 'plainTextEdit')
        self.txtVideoThree= self.findChild(QtWidgets.QPlainTextEdit, 'plainTextEdit_2')

    def GetFileFirstpath(self):
        self.video_one_path = self.GetFilepath()

    def GetFileSecondpath(self):
        self.video_two_path = self.GetFilepath()

    def GetFileThirdpath(self):
        self.video_three_path = self.GetFilepath()

    def GetFilepath(self):
        # This is executed when the button is pressed
        openFileDialog = QFileDialog.getOpenFileName(self,"select Video File",os.getcwd(),"Video Files (*.mp4 *avi)")
        path = openFileDialog[0]
        print(f'path = {path}')
        return path

    def Detect(self):
        list_of_videos = []
        list_of_videos.append(self.video_one_path)
        list_of_videos.append(self.video_two_path)
        list_of_videos.append(self.video_three_path)
        zero = 0
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).autoshape()
        # img2 = cv2.imread('yolov5-master/data/images/bus.jpg')[:,:,::-1]
        # imgs = [img2]
        # # Inference
        # results = model(imgs, size=640)
        # results.print()
        # results.show()

    


app = QApplication([])
window = Ui_MainWindow()
window.show()
app.exec_()
