from app.detector.detector import PersonDetector
from app.tracker.tracker import PersonTracker
from app.event.line_counter import LineCounter
from app.database.database import Database
from app.database.attendance import Attendance
from config import *


def main():

    print("====================================")
    print(" Human Monitoring System")
    print(" Sprint 1 - Live Camera")
    print("====================================")

    detector = PersonDetector(YOLO_MODEL)
    tracker = PersonTracker(detector)
    line_counter = LineCounter()
    database = Database()
    attendance = Attendance(database)

    detector.open_camera(CAMERA_INDEX)

    while True:

        ret, frame = detector.read_frame()

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
                    attendance.save_event(
                        track_id=track_id,
                        event=event
                    )

                person_count += 1

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0,255,0),
                    2
                )

                cv2.putText(
                    frame,
                    f"ID {track_id}",
                    (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,0),
                    2
                )

        cv2.rectangle(
            frame,
            (10,10),
            (220,120),
            (0,0,0),
            -1
        )

        cv2.putText(
            frame,
            f"Person : {person_count}",
            (20,45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"Side : {current_side}",
            (x1, y2 + 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,255,0),
            2
        )

        cv2.putText(
            frame,
            f"IN : {line_counter.in_count}",
            (20,70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"OUT : {line_counter.out_count}",
            (20,100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,0,255),
            2
        )

        cv2.line(
            frame,
            line_counter.line_p1,
            line_counter.line_p2,
            (255,0,0),
            3
        )

        detector.show_frame(
            frame,
            WINDOW_NAME
        )

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