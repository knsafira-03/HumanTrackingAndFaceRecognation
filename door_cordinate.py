import cv2

from app_config import CAMERA_INDEX


def click_event(event, x, y, flags, params):

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Koordinat Diklik -> X: {x}, Y: {y}")


def main():

    cap = cv2.VideoCapture(CAMERA_INDEX)

    cv2.namedWindow("Setting Garis Pintu")
    cv2.setMouseCallback("Setting Garis Pintu", click_event)

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Frame tidak terbaca")
            break

        cv2.putText(
            frame,
            "Klik Ujung Kiri dan Kanan Pintu untuk Tahu Koordinat X,Y",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        cv2.imshow("Setting Garis Pintu", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()