import pickle
import cv2

from app.recognition.face_recognizer import FaceRecognizer


print("=" * 40)
print("Face Recognition Test")
print("=" * 40)

# Load embeddings
with open("embeddings.pkl", "rb") as f:
    known_faces = pickle.load(f)

recognizer = FaceRecognizer()

# Ganti nama file jika ingin menguji foto lain
image = cv2.imread("test_images/raras_test.jpeg")

name, score = recognizer.recognize(
    image,
    known_faces
)

print()
print("Prediction :", name)
print("Distance   :", round(score, 4))