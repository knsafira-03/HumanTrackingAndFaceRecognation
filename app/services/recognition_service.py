import cv2

from app.detector.face_detector import FaceDetector
from app.recognition.face_matcher import FaceMatcher
from app.recognition.face_recognizer import FaceRecognizer
from app.recognition.track_registry import TrackRegistry
from app.recognition.face_database import FaceDatabase

from app_config import *


class RecognitionService:

    def __init__(self):

        print("[INFO] Initializing Recognition Service...")

        self.face_detector = FaceDetector(FACE_MODEL)

        self.face_matcher = FaceMatcher()

        self.face_recognizer = FaceRecognizer()

        self.face_database = FaceDatabase(
            "photos",
            self.face_recognizer.model
        )

        self.known_faces = self.face_database.build()

        self.registry = TrackRegistry()

        print("[INFO] Recognition Service Ready")

    def recognize(
        self,
        frame,
        person_box,
        track_id
    ):
        print(f"[TRACK] {track_id}")

        face_results = self.face_detector.detect(
            frame,
            FACE_CONFIDENCE
        )

        for result in face_results:

            boxes = result.boxes.xyxy.cpu().numpy()

            for face_box in boxes:

                face_box = tuple(map(int, face_box))

                if not self.face_matcher.match(
                    person_box,
                    face_box
                ):
                    continue

                fx1, fy1, fx2, fy2 = face_box

                h, w = frame.shape[:2]

                fx1 = max(0, fx1)
                fy1 = max(0, fy1)
                fx2 = min(w, fx2)
                fy2 = min(h, fy2)

                face_crop = frame[
                    fy1:fy2,
                    fx1:fx2
                ]

                if face_crop.size == 0:
                    continue

                name, score = self.face_recognizer.recognize(
                    face_crop,
                    self.known_faces
                )

                self.registry.update(
                    track_id,
                    name,
                    score
                )

                print(
                    f"[FACE] "
                    f"Track {track_id} "
                    f"-> {name} "
                    f"({score:.3f})"
                )

                return name

        self.registry.update(
            track_id,
            "Unknown",
            999
        )

        return "Unknown"