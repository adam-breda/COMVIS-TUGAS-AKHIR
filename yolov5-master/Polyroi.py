import cv2
import imutils
import numpy as np
import joblib
import matplotlib.path as mplPath

class PolyROI():
    roi_pts = []
    def MakeROI(self,img):
        self.img = img
        # if(self.img != None):
        print("Image Loaded")
        cv2.namedWindow('makeROI')
        cv2.setMouseCallback('makeROI', self.draw_roi)

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break
        cv2.destroyAllWindows()
        self.poly_path = mplPath.Path(np.array(self.roi_pts))
        return self.roi_pts
        # else:
        #     print("Fail to load image!")
        #     return None

    def draw_roi(self,event, x, y, flags, param):
            img2 = self.img.copy()

            if event == cv2.EVENT_LBUTTONDOWN:
                self.roi_pts.append((x, y))  

            if event == cv2.EVENT_RBUTTONDOWN:
                self.roi_pts.pop()  

            if event == cv2.EVENT_MBUTTONDOWN:
                mask = np.zeros(self.img.shape, np.uint8)
                points = np.array(self.roi_pts, np.int32)
                points = points.reshape((-1, 1, 2))
                # 画多边形
                mask = cv2.polylines(mask, [points], True, (255, 255, 255), 2)
                mask2 = cv2.fillPoly(mask.copy(), [points], (255, 255, 255))
                mask3 = cv2.fillPoly(mask.copy(), [points], (0, 255, 0))

                show_image = cv2.addWeighted(src1=self.img, alpha=0.8, src2=mask3, beta=0.2, gamma=0)

                cv2.imshow("mask", mask2)
                cv2.imshow("show_img", show_image)

                ROI = cv2.bitwise_and(mask2, self.img)
                cv2.imshow("ROI", ROI)
                cv2.waitKey(0)

            if len(self.roi_pts) > 0:
                cv2.circle(img2, self.roi_pts[-1], 3, (0, 0, 255), -1)

            if len(self.roi_pts) > 1:
                for i in range(len(self.roi_pts) - 1):
                    cv2.circle(img2, self.roi_pts[i], 5, (0, 0, 255), -1)
                    cv2.line(img=img2, pt1=self.roi_pts[i], pt2=self.roi_pts[i + 1], color=(255, 0, 0), thickness=2)
            cv2.imshow('makeROI', img2)

    def checkInside(self,point):
        if(self.poly_path.contains_point(point)):
            return 1
        else:
            return 0
