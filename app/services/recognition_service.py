from app.detector.face_detector import FaceDetector
from app.recognition.face_matcher import FaceMatcher
from app.recognition.face_recognizer import FaceRecognizer
from app.recognition.track_registry import TrackRegistry
from app.recognition.face_database import FaceDatabase

from app_config import *


class RecognitionService:

    def __init__(self):

        print("[INFO] Initializing Recognition Service...")

        # ==========================================
        # FACE DETECTOR
        # ==========================================

        self.face_detector = FaceDetector(
            FACE_MODEL
        )

        # ==========================================
        # FACE MATCHER
        # ==========================================

        self.face_matcher = FaceMatcher()

        # ==========================================
        # FACENET
        # ==========================================

        self.face_recognizer = FaceRecognizer()

        # ==========================================
        # FACE DATABASE
        # ==========================================

        self.face_database = FaceDatabase(
            "photos",
            self.face_recognizer.model
        )

        self.known_faces = self.face_database.build()

        # ==========================================
        # TRACK REGISTRY
        # ==========================================

        self.registry = TrackRegistry(
            votes_required=FACE_LOCK_VOTES,
            history_size=FACE_VOTE_HISTORY
        )

        print("[INFO] Recognition Service Ready")

    # ==============================================
    # RECOGNITION
    # ==============================================

    def recognize(
        self,
        frame,
        person_box,
        track_id
    ):

        # ==========================================
        # 1. CHECK LOCKED IDENTITY
        # ==========================================

        if self.registry.is_locked(track_id):

            name = self.registry.get_name(
                track_id
            )

            distance = self.registry.get_confidence(
                track_id
            )

            print(
                f"[LOCKED] "
                f"Track {track_id} "
                f"-> {name} "
                f"({distance:.3f})"
            )

            return name, None

        # ==========================================
        # 2. DETECT FACE
        # ==========================================

        face_results = self.face_detector.detect(
            frame,
            FACE_CONFIDENCE
        )

        # ==========================================
        # 3. FIND FACE BELONGING TO PERSON
        # ==========================================

        for result in face_results:

            if result.boxes is None:
                continue

            boxes = result.boxes.xyxy.cpu().numpy()

            for face_box in boxes:

                face_box = tuple(
                    map(int, face_box)
                )

                # ==================================
                # CHECK FACE INSIDE PERSON BOX
                # ==================================

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

                # ==================================
                # FACE RECOGNITION
                # ==================================

                name, distance = (
                    self.face_recognizer.recognize(
                        face_crop,
                        self.known_faces
                    )
                )

                # ==================================
                # UNKNOWN
                # ==================================

                if name == "Unknown":

                    print(
                        f"[FACE] "
                        f"Track {track_id} "
                        f"-> Unknown"
                    )

                    # Jangan menghapus candidate
                    return "Unknown", face_crop

                # ==================================
                # UPDATE CANDIDATE
                # ==================================

                self.registry.update(
                    track_id,
                    name,
                    distance
                )

                candidate_count = (
                    self.registry
                    .get_candidate_count(track_id)
                )

                print(
                    f"[FACE] "
                    f"Track {track_id} "
                    f"-> {name} "
                    f"distance={distance:.3f} "
                    f"confirmation="
                    f"{candidate_count}/3"
                )

                # ==================================
                # CHECK LOCK
                # ==================================

                if self.registry.is_locked(
                    track_id
                ):

                    print(
                        f"[LOCK] "
                        f"Track {track_id} "
                        f"IDENTITY LOCKED -> {name}"
                    )

                    return name, face_crop

                # Belum locked
                return name, face_crop

        # ==========================================
        # 4. FACE TIDAK TERLIHAT
        # ==========================================

        if self.registry.has(track_id):

            # Kalau sebelumnya sudah pernah punya
            # candidate, jangan hapus candidate.

            if self.registry.is_locked(track_id):

                return (
                    self.registry.get_name(track_id),
                    None
                )

        return "Unknown", None