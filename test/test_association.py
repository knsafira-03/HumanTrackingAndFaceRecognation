import cv2

from app.detector.detector import PersonDetector
from app.detector.face_detector import FaceDetector
from app.recognition.face_matcher import FaceMatcher
from config import *

print("=" * 50)
print("Person - Face Association Test")
print("=" * 50)

person_detector = PersonDetector(YOLO_MODEL)
face_detector = FaceDetector(FACE_MODEL)
matcher = FaceMatcher()

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    person_results = person_detector.track(
        frame,
        CONFIDENCE,
        PERSON_CLASS,
        TRACKER
    )

    face_results = face_detector.detect(
        frame,
        FACE_CONFIDENCE
    )

    # -----------------------------
    # Ambil semua wajah
    # -----------------------------

    face_boxes = []

    for result in face_results:

        for box in result.boxes.xyxy.cpu().numpy():

            face_boxes.append(
                tuple(map(int, box))
            )

    # -----------------------------
    # Ambil semua orang
    # -----------------------------

    for result in person_results:

        if result.boxes.id is None:
            continue

        person_boxes = result.boxes.xyxy.cpu().numpy()

        ids = result.boxes.id.int().cpu().numpy()

        for person_box, track_id in zip(person_boxes, ids):

            person_box = tuple(map(int, person_box))

            px1, py1, px2, py2 = person_box

            cv2.rectangle(
                frame,
                (px1, py1),
                (px2, py2),
                (0,255,0),
                2
            )

            cv2.putText(
                frame,
                f"Person {track_id}",
                (px1, py1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2
            )

            # Cari wajah yang berada di dalam person box
            for face_box in face_boxes:

                if matcher.match(person_box, face_box):

                    fx1, fy1, fx2, fy2 = face_box

                    cv2.rectangle(
                        frame,
                        (fx1, fy1),
                        (fx2, fy2),
                        (255,0,0),
                        2
                    )

                    cv2.putText(
                        frame,
                        f"Face -> {track_id}",
                        (fx1, fy1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255,0,0),
                        2
                    )

                    print(f"Person {track_id} -> Face")

                    break

    cv2.imshow("Association Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()