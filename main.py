import cv2
import time
import os

from app.detector.detector import PersonDetector
from app.tracker.tracker import PersonTracker
from app.event.line_counter import LineCounter
from app.event.track_resolver import TrackIdentityResolver

from app.database.database import Database
from app.database.attendance import Attendance

from app.services.recognition_service import RecognitionService

from app.snapshot.snapshot_service import SnapshotService
from app.notification.notification_manager import NotificationManager
from app.utils.status_writer import write_status
from app.utils.hud import draw_hud

# from app.recognition.face_database import FaceDatabase
# from app.recognition.face_recognizer import FaceRecognizer
# from app.recognition.track_registry import TrackRegistry

from app_config import *


def main():

    print("====================================")
    print(" Human Monitoring System")
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

    # Menjembatani track_id yang "putus" gara-gara ByteTrack ganti ID
    # (oklusi, ganti pose, 2 orang berpapasan). Toleransi untuk identitas
    # locked TIDAK dibuat terlalu besar -- kalau kebesaran, begitu 2 orang
    # jalan berdekatan (misal keluar bareng), identitas yang satu bisa
    # "ketarik" salah nempel ke yang lain gara-gara jaraknya kebetulan
    # lebih dekat. lihat app/event/track_resolver.py untuk penjelasan.
    track_resolver = TrackIdentityResolver(
        is_locked_fn=recognition_service.registry.is_locked,
        max_distance=120,          # untuk track yang BELUM locked (ketat)
        max_age=2.0,
        locked_max_distance=180,   # untuk track yang SUDAH locked (agak longgar, TAPI TIDAK KEBESARAN)
        locked_max_age=4.0,
    )

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

        # ==================================
        # LANGKAH A: kumpulkan SEMUA orang di frame ini dulu, baru
        # sambungkan track_id yang putus SEKALIGUS (bukan satu-satu).
        # ==================================

        raw_detections = []  # (track_id, box, conf)
        positions_for_resolver = []  # (track_id, box_center)

        for result in results:

            if result.boxes.id is None:
                continue

            boxes = result.boxes.xyxy.cpu().numpy()

            ids = result.boxes.id.int().cpu().numpy()

            confs = result.boxes.conf.cpu().numpy()

            for box, track_id, conf in zip(boxes, ids, confs):

                raw_detections.append((track_id, box, conf))

                x1, y1, x2, y2 = map(int, box)

                box_center = (
                    int((x1 + x2) / 2),
                    int((y1 + y2) / 2)
                )

                positions_for_resolver.append((track_id, box_center))

        id_map = track_resolver.resolve_frame(positions_for_resolver)

        # ==================================
        # LANGKAH A.5: CEGAH 1 NAMA DIPEGANG 2 TRACK SEKALIGUS
        # ==================================
        # Bisa kejadian gara-gara track_resolver salah "mengadopsi"
        # identitas locked ke orang yang berbeda (misal 2 orang jalan
        # berdekatan). Kalau ini dibiarkan, 1 nama bisa nempel di 2
        # bounding box bersamaan -- padahal secara logika itu mustahil.
        # Yang confidence-nya lebih jelek di-reset paksa (registry.remove),
        # supaya dia mulai dari nol lagi (voting ulang), bukan menyamar
        # jadi nama orang lain.

        stable_ids_this_frame = set(id_map.values())

        name_to_stable_ids = {}

        for stable_id in stable_ids_this_frame:

            if recognition_service.registry.is_locked(stable_id):

                name = recognition_service.registry.get_name(stable_id)

                name_to_stable_ids.setdefault(name, []).append(stable_id)

        for name, ids_with_this_name in name_to_stable_ids.items():

            if len(ids_with_this_name) > 1:

                best_id = min(
                    ids_with_this_name,
                    key=lambda sid: recognition_service.registry.get_confidence(sid)
                )

                for sid in ids_with_this_name:

                    if sid != best_id:

                        print(
                            f"[CONFLICT] Nama '{name}' dipegang "
                            f"{len(ids_with_this_name)} track sekaligus "
                            f"(stable_id={sid} vs {best_id}, "
                            f"{best_id} dipertahankan) -- "
                            f"stable_id={sid} direset, dikenali ulang"
                        )

                        recognition_service.registry.remove(sid)

        # ==================================
        # LANGKAH B: proses tiap orang seperti biasa, pakai stable_id
        # ==================================

        for track_id, box, conf in raw_detections:

                x1, y1, x2, y2 = map(int, box)

                foot_x = int((x1 + x2) / 2)
                foot_y = int(y2)

                stable_id = id_map[track_id]

                print(
                    f"[TRACK] "
                    f"raw={track_id} stable={stable_id} "
                    f"({x1},{y1})"
                )

                name, face_crop = recognition_service.recognize(
                    frame,
                    (x1, y1, x2, y2),
                    stable_id
                )

                # ==================================
                # LINE COUNTER
                # ==================================

                current_side = line_counter.get_side(
                    (foot_x, foot_y)
                )

                event = line_counter.update(
                    stable_id,
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

                    raw_distance = recognition_service.registry.get_confidence(stable_id)

                    if name == "Unknown" or raw_distance is None:
                        confidence_pct = None
                    else:
                        confidence_pct = round(max(0, 1 - raw_distance) * 100, 2)

                    attendance.save_event(
                        track_id=stable_id,
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
                    f"{name} | ID {stable_id} | {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
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

        # ==========================================
        # HUD (panel Person/Masuk/Keluar/FPS)
        # ==========================================

        draw_hud(
            frame,
            person_count,
            line_counter.in_count,
            line_counter.out_count,
            fps
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