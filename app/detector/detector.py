from ultralytics import YOLO
import cv2

class PersonDetector:

    def __init__(self,
                 model_path,
                 camera_index=0):

        self.model = YOLO(model_path)

        self.cap = cv2.VideoCapture(camera_index)

    def read_frame(self):

        return self.cap.read()

    def release(self):

        self.cap.release()