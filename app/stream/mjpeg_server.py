from flask import Flask, Response
import cv2
import threading

from app.stream.stream_service import StreamService


app = Flask(__name__)

stream_service = StreamService()


def generate():

    while True:

        frame = stream_service.get_frame()

        if frame is None:
            continue

        _, buffer = cv2.imencode(".jpg", frame)

        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes +
            b"\r\n"
        )


@app.route("/video_feed")
def video_feed():

    return Response(
        generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


def start_server():

    threading.Thread(
        target=lambda: app.run(
            host="0.0.0.0",
            port=5000,
            threaded=True,
            debug=False,
            use_reloader=False
        ),
        daemon=True
    ).start()