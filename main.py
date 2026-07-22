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

        results = detector.track(
            frame,
            CONFIDENCE,
            PERSON_CLASS,
            TRACKER
        )

        person_count = 0

        for result in results:

            for box in result.boxes:

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                conf = float(box.conf[0])

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
                    f"Person {conf:.2f}",
                    (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0,255,0),
                    2
                )
        cv2.rectangle(
            frame,
            (10,10),
            (220,60),
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