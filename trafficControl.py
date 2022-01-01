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
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QAction, QMainWindow, QSlider, QPushButton, QToolTip, QApplication,QLCDNumber
import torch


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('Traffic.ui', self)
        self.txtVehicleRoad1 = self.findChild(QtWidgets.QPlainTextEdit, 'input_vehicle1')
        self.txtVehicleRoad2 = self.findChild(QtWidgets.QPlainTextEdit, 'input_vehicle2')
        self.txtVehicleRoad3 = self.findChild(QtWidgets.QPlainTextEdit, 'input_vehicle3')
        self.lcdRoad1 = self.findChild(QtWidgets.QLCDNumber, 'lcd_road1')
        self.lcdRoad1.display(60)
        self.lcdRoad2 = self.findChild(QtWidgets.QLCDNumber, 'lcd_road2')
        self.lcdRoad2.display(60)
        self.lcdRoad3 = self.findChild(QtWidgets.QLCDNumber, 'lcd_road3')
        self.lcdRoad3.display(60)
        self.btnUpdateTimer = self.findChild(QtWidgets.QPushButton, 'btn_update_timer')
        self.roadCount = 3
        self.btnUpdateTimer.clicked.connect(self.updateTimer)

    def updateTimer(self):
        roadCount = self.roadCount
        firstCount = int(self.txtVehicleRoad1.toPlainText())
        secondCount  = int(self.txtVehicleRoad2.toPlainText())
        thirdCount  = int(self.txtVehicleRoad3.toPlainText())
        sumRoadVehicle = firstCount + secondCount + thirdCount
        firstCount = firstCount / sumRoadVehicle * 60 *roadCount
        secondCount = secondCount / sumRoadVehicle * 60 *roadCount
        thirdCount = thirdCount / sumRoadVehicle * 60 *roadCount
        self.UpdateLCD(self.lcdRoad1,firstCount)
        self.UpdateLCD(self.lcdRoad2,secondCount)
        self.UpdateLCD(self.lcdRoad3,thirdCount)

    def UpdateLCD(self,lcd,timer):
        lcd.display(timer)

    def timeAdjustment(count):
        return 0

    # def GetFilepath(self):
    #     # This is executed when the button is pressed
    #     openFileDialog = QFileDialog.getOpenFileName(self,"select Video File",os.getcwd(),"Video Files (*.mp4 *avi)")
    #     path = openFileDialog[0]
    #     print(f'path = {path}')
    #     return path

    # def Detect(self):
    #     list_of_videos = []
    #     list_of_videos.append(self.video_one_path)
    #     list_of_videos.append(self.video_two_path)
    #     list_of_videos.append(self.video_three_path)
    #     zero = 0
    #     model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).autoshape()
    #     # img2 = cv2.imread('yolov5-master/data/images/bus.jpg')[:,:,::-1]
    #     # imgs = [img2]
    #     # # Inference
    #     # results = model(imgs, size=640)
    #     # results.print()
    #     # results.show()

    


app = QApplication([])
window = Ui_MainWindow()
window.show()
app.exec_()
