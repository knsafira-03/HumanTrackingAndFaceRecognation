import os
import cv2
import numpy as np


class FaceDatabase:

    def __init__(self, dataset_path, embedder):

        self.dataset_path = dataset_path
        self.embedder = embedder

        self.embeddings = {}

    def build(self):

        print("[INFO] Building Face Database...")

        for file in os.listdir(self.dataset_path):

            if not file.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            name = os.path.splitext(file)[0]

            image_path = os.path.join(self.dataset_path, file)

            image = cv2.imread(image_path)

            if image is None:
                continue

            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            embedding = self.embedder.embeddings([rgb])[0]

            self.embeddings[name] = embedding

            print(f"[EMBEDDING] {name}")

        print(f"[INFO] {len(self.embeddings)} wajah berhasil dibuat.")

        return self.embeddings