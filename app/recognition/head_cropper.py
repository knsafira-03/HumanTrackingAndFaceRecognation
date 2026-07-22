import cv2


class HeadCropper:

    def crop(self, frame, box):

        x1, y1, x2, y2 = map(int, box)

        width = x2 - x1
        height = y2 - y1

        # Ambil sekitar 40% bagian atas tubuh
        head_bottom = y1 + int(height * 0.4)

        face = frame[
            max(0, y1):head_bottom,
            max(0, x1):min(frame.shape[1], x2)
        ]

        return face