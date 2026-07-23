import os
import cv2

from datetime import datetime


class SnapshotService:

    def __init__(self, folder="snapshots"):

        self.folder = folder

        os.makedirs(
            self.folder,
            exist_ok=True
        )

    def save(
        self,
        frame,
        name,
        direction
    ):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            f"{timestamp}_"
            f"{name.lower()}_"
            f"{direction.lower()}.jpg"
        )

        filepath = os.path.join(
            self.folder,
            filename
        )

        cv2.imwrite(
            filepath,
            frame
        )

        print(
            f"[SNAPSHOT] {filename}"
        )

        return filepath