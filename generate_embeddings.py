import pickle

from app.recognition.face_database import FaceDatabase
from app.recognition.face_recognizer import FaceRecognizer


def main():

    print("=" * 40)
    print("Generate Face Embeddings")
    print("=" * 40)

    recognizer = FaceRecognizer()

    database = FaceDatabase(
        "photos",
        recognizer.model
    )

    embeddings = database.build()

    with open("embeddings.pkl", "wb") as f:
        pickle.dump(embeddings, f)

    print()
    print(f"[INFO] {len(embeddings)} embeddings berhasil disimpan.")
    print("[INFO] File : embeddings.pkl")


if __name__ == "__main__":
    main()