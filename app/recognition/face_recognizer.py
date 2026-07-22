from keras_facenet import FaceNet
from scipy.spatial.distance import cosine
import cv2


class FaceRecognizer:

    def __init__(self):

        print("[INFO] Loading FaceNet...")

        self.model = FaceNet()

        print("[INFO] FaceNet Loaded")

    def generate_embedding(self, image):

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        embedding = self.model.embeddings([rgb])[0]

        return embedding

    def recognize(self, image, known_faces, threshold=0.65):

        embedding = self.generate_embedding(image)

        best_name = "Unknown"
        best_score = 999

        for name, saved_embedding in known_faces.items():

            score = cosine(embedding, saved_embedding)

            print(f"{name:<10} -> {score:.3f}")

            if score < best_score:
                best_score = score
                best_name = name

        print(f"Best Match : {best_name}")
        print(f"Distance   : {best_score:.3f}")

        if best_score > threshold:
            print("Status     : Unknown")
            best_name = "Unknown"
        else:
            print("Status     : Accepted")

        print("-" * 40)

        return best_name, best_score