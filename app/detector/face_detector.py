from ultralytics import YOLO


class FaceDetector:

    def __init__(self, model_path):

        print("[INFO] Loading YOLO Face...")

        self.model = YOLO(model_path)

        print("[INFO] YOLO Face Loaded")

    def detect(self, frame, conf=0.5):

        results = self.model(
            frame,
            conf=conf,
            verbose=False
        )

        return results