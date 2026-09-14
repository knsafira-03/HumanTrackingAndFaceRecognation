import cv2
import time
import os

from app.detector.detector import PersonDetector
from app.tracker.tracker import PersonTracker
from app.event.line_counter import LineCounter

from app.database.database import Database
from app.database.attendance import Attendance

from app.services.recognition_service import RecognitionService

from app.snapshot.snapshot_service import SnapshotService
from app.notification.notification_manager import NotificationManager
from app.utils.status_writer import write_status

# from app.recognition.face_database import FaceDatabase
# from app.recognition.face_recognizer import FaceRecognizer
# from app.recognition.track_registry import TrackRegistry

from app_config import *


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
    notification = NotificationManager()

    # face_recognizer = FaceRecognizer()

    # face_database = FaceDatabase(
    #     "photos",
    #     face_recognizer.model
    # )

    # known_faces = face_database.build()

    # track_registry = TrackRegistry()

    detector.open_camera(CAMERA_INDEX)

    # semua modul berhasil di-init -> laporkan status awal ke dashboard
    write_status(
        yolo_engine=True,
        face_recognition=True,
        whatsapp=True,
    )

    # supaya tidak error ketika frame pertama kosong
    current_side = 0

    # status koneksi WhatsApp yang SEBENARNYA (bukan hardcode True terus),
    # di-update tiap ada event terkirim, dilaporkan ke dashboard lewat
    # write_status() di bawah.
    last_whatsapp_ok = True

    # ==========================================
    # MAIN LOOP
    # ==========================================
    prev_time = time.time()

    last_preview_save = 0
    last_status_write = time.time()

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

                name, face_crop = recognition_service.recognize(
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

                    snapshot = face_crop if face_crop is not None else person_crop

                    snapshot_path = snapshot_service.save(
                        snapshot,
                        name,
                        event
                    )

                    # Ambil confidence (cosine distance) dari registry yang
                    # dipakai recognition_service, lalu ubah jadi persentase
                    # yang gampang dibaca di dashboard (0 distance = 100%,
                    # makin besar distance makin rendah persentasenya).
                    # Ini metrik pendekatan, bukan probabilitas statistik
                    # yang presisi -- tapi cukup buat indikasi di UI.
                    raw_distance = recognition_service.registry.get_confidence(track_id)

                    if name == "Unknown" or raw_distance is None:
                        confidence_pct = None
                    else:
                        confidence_pct = round(max(0, 1 - raw_distance) * 100, 2)

                    attendance.save_event(
                        track_id=track_id,
                        direction=event,
                        name=name,
                        snapshot_path=snapshot_path,
                        confidence=confidence_pct
                    )

                    status = (
                        "UNAUTHORIZED"
                        if name == "Unknown"
                        else "AUTHORIZED"
                    )

                    try:
                        result = notification.send_event(
                            name=name,
                            status=status,
                            direction=event,
                            snapshot_path=snapshot_path
                        )
                        last_whatsapp_ok = bool(result.get("status", False))

                    except Exception as e:
                        print(f"[NOTIFICATION] Gagal kirim notifikasi: {e}")
                        last_whatsapp_ok = False

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

        # ==========================================
        # HEARTBEAT
        # ==========================================

        if time.time() - last_status_write > 3:

            write_status(
                yolo_engine=True,
                face_recognition=True,
                whatsapp=last_whatsapp_ok,
            )

            last_status_write = time.time()

        # ==========================================
        # LIVE PREVIEW
        # ==========================================

        if time.time() - last_preview_save > 0.5:

            os.makedirs("static", exist_ok=True)

            cv2.imwrite(
                "static/live.jpg",
                frame
            )

            last_preview_save = time.time()

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