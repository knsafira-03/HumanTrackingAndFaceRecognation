import cv2

from app.detector.face_detector import FaceDetector
from config import *

print("=" * 40)
print("YOLO Face Detector Test")
print("=" * 40)

detector = FaceDetector(FACE_MODEL)

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = detector.detect(
        frame,
        FACE_CONFIDENCE
    )

    for result in results:

        boxes = result.boxes.xyxy.cpu().numpy()

        confs = result.boxes.conf.cpu().numpy()

        for box, conf in zip(boxes, confs):

            x1, y1, x2, y2 = map(int, box)

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"{conf:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    cv2.imshow("YOLO Face", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()