from ultralytics import YOLO
import cv2
import os


class PersonDetector:

    def __init__(self, model_path):

        self.model = YOLO(model_path)

        self.cap = None

    def open_camera(self, camera_index):

        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise Exception("Camera gagal dibuka.")

    def read_frame(self):

        return self.cap.read()

    def release(self):

        if self.cap is not None:
            self.cap.release()