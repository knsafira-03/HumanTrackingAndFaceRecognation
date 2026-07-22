from app.detector.detector import PersonDetector
from config import *

def main():

    print("====================================")
    print(" Human Monitoring System")
    print(" Sprint 1 - Detector Module")
    print("====================================")

    detector = PersonDetector(YOLO_MODEL)

    detector.open_camera(CAMERA_INDEX)

    detector.release()

    print("\nDetector Module Success")

if __name__ == "__main__":
    main()