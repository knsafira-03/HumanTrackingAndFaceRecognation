import cv2

from app.recognition.head_cropper import HeadCropper

cropper = HeadCropper()

image = cv2.imread("photos/khalisa.jpeg")

h, w = image.shape[:2]

# Simulasi bounding box YOLO
box = (
    0,
    0,
    w,
    h
)

face = cropper.crop(
    image,
    box
)

cv2.imshow("Original", image)
cv2.imshow("Head Crop", face)

cv2.waitKey(0)
cv2.destroyAllWindows()