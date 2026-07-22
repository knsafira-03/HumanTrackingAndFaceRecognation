from app.detector.detector import PersonDetector
from config import *


def main():

    print("====================================")
    print(" Human Monitoring System")
    print(" Sprint 1 - Live Camera")
    print("====================================")

    detector = PersonDetector(YOLO_MODEL)

    detector.open_camera(CAMERA_INDEX)

    while True:

        ret, frame = detector.read_frame()

        if not ret:
            print("Frame tidak terbaca")
            break

        detector.show_frame(frame, WINDOW_NAME)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    detector.release()

    print("Program selesai")


if __name__ == "__main__":
    import cv2
    main()