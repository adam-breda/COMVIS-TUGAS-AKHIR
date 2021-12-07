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
        list_of_vehicles = ["bicycle","car","motorbike","bus","truck", "train"]
        list_of_videos.append(self.video_one_path)
        list_of_videos.append(self.video_two_path)
        list_of_videos.append(self.video_three_path)
    
    def displayVehicleCount(frame, vehicle_count):
        cv2.putText(
            frame, #Image
            'Detected Vehicles: ' + str(vehicle_count), #Label
            (20, 20), #Position
            cv2.FONT_HERSHEY_SIMPLEX, #Font
            1, #Size
            (0, 0xFF, 0), #Color
            2, #Thickness
            cv2.FONT_HERSHEY_COMPLEX_SMALL,
            )

# PURPOSE: Determining if the box-mid point cross the line or are within the range of 5 units
# from the line
# PARAMETERS: X Mid-Point of the box, Y mid-point of the box, Coordinates of the line 
# RETURN: 
# - True if the midpoint of the box overlaps with the line within a threshold of 5 units 
# - False if the midpoint of the box lies outside the line and threshold
def boxAndLineOverlap(x_mid_point, y_mid_point, line_coordinates):
	x1_line, y1_line, x2_line, y2_line = line_coordinates #Unpacking

	if (x_mid_point >= x1_line and x_mid_point <= x2_line+5) and\
		(y_mid_point >= y1_line and y_mid_point <= y2_line+5):
		return True
	return False

# PURPOSE: Displaying the FPS of the detected video
# PARAMETERS: Start time of the frame, number of frames within the same second
# RETURN: New start time, new number of frames 
def displayFPS(start_time, num_frames):
	current_time = int(time.time())
	if(current_time > start_time):
		os.system('cls') # Equivalent of CTRL+L on the terminal
		print("FPS:", num_frames)
		num_frames = 0
		start_time = current_time
	return start_time, num_frames

# PURPOSE: Draw all the detection boxes with a green dot at the center
# RETURN: N/A
def drawDetectionBoxes(idxs, boxes, classIDs, confidences, frame):
	# ensure at least one detection exists
	if len(idxs) > 0:
		# loop over the indices we are keeping
		for i in idxs.flatten():
			# extract the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])

			# draw a bounding box rectangle and label on the frame
			color = [int(c) for c in COLORS[classIDs[i]]]
			cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
			text = "{}: {:.4f}".format(LABELS[classIDs[i]],
				confidences[i])
			cv2.putText(frame, text, (x, y - 5),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
			#Draw a green dot in the middle of the box
			cv2.circle(frame, (x + (w//2), y+ (h//2)), 2, (0, 0xFF, 0), thickness=2)

# PURPOSE: Initializing the video writer with the output video path and the same number
# of fps, width and height as the source video 
# PARAMETERS: Width of the source video, Height of the source video, the video stream
# RETURN: The initialized video writer
def initializeVideoWriter(video_width, video_height, videoStream):
	# Getting the fps of the source video
	sourceVideofps = videoStream.get(cv2.CAP_PROP_FPS)
	# initialize our video writer
	fourcc = cv2.VideoWriter_fourcc(*"MJPG")
	return cv2.VideoWriter(outputVideoPath, fourcc, sourceVideofps,
		(video_width, video_height), True)

# PURPOSE: Identifying if the current box was present in the previous frames
# PARAMETERS: All the vehicular detections of the previous frames, 
#			the coordinates of the box of previous detections
# RETURN: True if the box was current box was present in the previous frames;
#		  False if the box was not present in the previous frames
def boxInPreviousFrames(previous_frame_detections, current_box, current_detections):
	centerX, centerY, width, height = current_box
	dist = np.inf #Initializing the minimum distance
	# Iterating through all the k-dimensional trees
	for i in range(FRAMES_BEFORE_CURRENT):
		coordinate_list = list(previous_frame_detections[i].keys())
		if len(coordinate_list) == 0: # When there are no detections in the previous frame
			continue
		# Finding the distance to the closest point and the index
		temp_dist, index = spatial.KDTree(coordinate_list).query([(centerX, centerY)])
		if (temp_dist < dist):
			dist = temp_dist
			frame_num = i
			coord = coordinate_list[index[0]]

	if (dist > (max(width, height)/2)):
		return False

	# Keeping the vehicle ID constant
	current_detections[(centerX, centerY)] = previous_frame_detections[frame_num][coord]
	return True

def count_vehicles(idxs, boxes, classIDs, vehicle_count, previous_frame_detections, frame):
	current_detections = {}
	# ensure at least one detection exists
	if len(idxs) > 0:
		# loop over the indices we are keeping
		for i in idxs.flatten():
			# extract the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])
			
			centerX = x + (w//2)
			centerY = y+ (h//2)

			# When the detection is in the list of vehicles, AND
			# it crosses the line AND
			# the ID of the detection is not present in the vehicles
			if (LABELS[classIDs[i]] in list_of_vehicles):
				current_detections[(centerX, centerY)] = vehicle_count 
				if (not boxInPreviousFrames(previous_frame_detections, (centerX, centerY, w, h), current_detections)):
					vehicle_count += 1
					# vehicle_crossed_line_flag += True
				# else: #ID assigning
					#Add the current detection mid-point of box to the list of detected items
				# Get the ID corresponding to the current detection

				ID = current_detections.get((centerX, centerY))
				# If there are two detections having the same ID due to being too close, 
				# then assign a new ID to current detection.
				if (list(current_detections.values()).count(ID) > 1):
					current_detections[(centerX, centerY)] = vehicle_count
					vehicle_count += 1 

				#Display the ID at the center of the box
				cv2.putText(frame, str(ID), (centerX, centerY),\
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,255], 2)

	return vehicle_count, current_detections

    


app = QApplication([])
window = Ui_MainWindow()
window.show()
app.exec_()
