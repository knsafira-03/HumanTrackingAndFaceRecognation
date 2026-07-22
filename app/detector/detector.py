from ultralytics import YOLO
import cv2


class PersonDetector:

    def __init__(self, model_path):

        print("[INFO] Loading YOLO...")
        self.model = YOLO(model_path)
        print("[INFO] YOLO Loaded")

        self.cap = None

    def open_camera(self, camera_index):

        print("[INFO] Opening Camera...")

        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise Exception("Camera gagal dibuka.")

        print("[INFO] Camera Opened")

    def read_frame(self):

        return self.cap.read()

    def show_frame(self, frame, window_name):

        cv2.imshow(window_name, frame)

    def release(self):

        if self.cap is not None:
            self.cap.release()

        cv2.destroyAllWindows()