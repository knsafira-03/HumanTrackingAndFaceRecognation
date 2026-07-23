import os
import requests

from config.settings import FONNTE_TOKEN


class WhatsAppService:

    def send_message(
        self,
        target,
        message
    ):

        url = "https://api.fonnte.com/send"

        headers = {
            "Authorization": FONNTE_TOKEN
        }

        payload = {
            "target": target,
            "message": message
        }

        response = requests.post(
            url,
            headers=headers,
            data=payload
        )

        return response.json()


    def send_image(
        self,
        target,
        message,
        image_path
    ):

        url = "https://api.fonnte.com/send"

        headers = {
            "Authorization": FONNTE_TOKEN
        }

        if not os.path.exists(image_path):
            return {
                "status": False,
                "detail": "Image not found"
            }

        payload = {
            "target": target,
            "message": message
        }

        files = {
            "file": open(image_path, "rb")
        }

        response = requests.post(
            url,
            headers=headers,
            data=payload,
            files=files
        )

        files["file"].close()

        return response.json()