import cv2
import time

from app.detector.detector import PersonDetector
from app.tracker.tracker import PersonTracker
from app.event.line_counter import LineCounter

from app.database.database import Database
from app.database.attendance import Attendance

from app.services.recognition_service import RecognitionService

from app.snapshot.snapshot_service import SnapshotService

# from app.recognition.face_database import FaceDatabase
# from app.recognition.face_recognizer import FaceRecognizer
# from app.recognition.track_registry import TrackRegistry

from config import *


def main():

    print("====================================")
    print(" Human Monitoring System")
    print(" Sprint 1 - Live Camera")
    print("====================================")

    # ==========================================
    # INIT MODULE
    # ==========================================

    detector = PersonDetector(YOLO_MODEL)
    tracker = PersonTracker(detector)

    line_counter = LineCounter()

    database = Database()
    attendance = Attendance(database)

    recognition_service = RecognitionService()
    snapshot_service = SnapshotService()

    # face_recognizer = FaceRecognizer()

    # face_database = FaceDatabase(
    #     "photos",
    #     face_recognizer.model
    # )

    # known_faces = face_database.build()

    # track_registry = TrackRegistry()

    detector.open_camera(CAMERA_INDEX)

    # supaya tidak error ketika frame pertama kosong
    current_side = 0

    # ==========================================
    # MAIN LOOP
    # ==========================================
    prev_time = time.time()

    while True:

        ret, frame = detector.read_frame()

        if not ret:
            print("Frame tidak terbaca")
            break

        results = detector.track(
            frame,
            CONFIDENCE,
            PERSON_CLASS,
            TRACKER
        )

        person_count = 0

        for result in results:

            if result.boxes.id is None:
                continue

            boxes = result.boxes.xyxy.cpu().numpy()

            ids = result.boxes.id.int().cpu().numpy()

            confs = result.boxes.conf.cpu().numpy()

            for box, track_id, conf in zip(boxes, ids, confs):

                x1, y1, x2, y2 = map(int, box)

                # ==================================
                # TRACK REGISTRY
                # ==================================
                print(
                    f"[TRACK] "
                    f"{track_id} "
                    f"({x1},{y1})"
                )
                
                name = recognition_service.recognize(
                    frame,
                    (x1, y1, x2, y2),
                    track_id
                )

                # ==================================
                # LINE COUNTER
                # ==================================

                foot_x = int((x1 + x2) / 2)
                foot_y = int(y2)

                current_side = line_counter.get_side(
                    (foot_x, foot_y)
                )

                event = line_counter.update(
                    track_id,
                    current_side
                )

                if event is not None:
                    h, w = frame.shape[:2]

                    x1 = max(0, x1)
                    y1 = max(0, y1)

                    x2 = min(w, x2)
                    y2 = min(h, y2)

                    person_crop = frame[
                        y1:y2,
                        x1:x2
                    ]

                    snapshot_path = snapshot_service.save(
                        person_crop,
                        name,
                        event
                    )

                    attendance.save_event(
                        track_id=track_id,
                        direction=event,
                        name=name,
                        snapshot_path=snapshot_path
                    )

                person_count += 1

                # ==================================
                # DRAW BOX
                # ==================================

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"{name} | ID {track_id} | {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

        # ==========================================
        # DASHBOARD
        # ==========================================

        cv2.rectangle(
            frame,
            (10, 10),
            (230, 120),
            (0, 0, 0),
            -1
        )

        cv2.putText(
            frame,
            f"Person : {person_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"IN : {line_counter.in_count}",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"OUT : {line_counter.out_count}",
            (20, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

        # ==========================================
        # LINE
        # ==========================================

        cv2.line(
            frame,
            line_counter.line_p1,
            line_counter.line_p2,
            (255, 0, 0),
            3
        )

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        cv2.putText(
            frame,
            f"FPS : {fps:.1f}",
            (20, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2
        )

        detector.show_frame(
            frame,
            WINDOW_NAME
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    detector.release()

    print("Program selesai")


if __name__ == "__main__":
    main()