from app.detector.detector import PersonDetector
from config import *

def main():

    print("================================")
    print(" Human Monitoring System")
    print(" Sprint 1 - Detector Test")
    print("================================")

    detector = PersonDetector(
        YOLO_MODEL,
        CAMERA_INDEX
    )

    print("YOLO Loaded")

    if detector.cap.isOpened():
        print("Camera OK")
    else:
        print("Camera Failed")

    detector.release()

    print("Detector Module Success")

if __name__ == "__main__":
    main()