import logging
import multiprocessing
import os
import io
import cv2
import flask

from . import common

logging.basicConfig(level=logging.DEBUG)


VIDEO_SCREEN_WIDTH = int(os.environ.get("VIDEO_SCREEN_WIDTH", "640"))
VIDEO_SCREEN_HEIGHT = int(os.environ.get("VIDEO_SCREEN_HEIGHT", "480"))
UDPSRC_PORT = int(os.environ.get("UDPSRC_PORT", "6000"))

VIDEO_SCREEN_SIZE = (VIDEO_SCREEN_WIDTH, VIDEO_SCREEN_HEIGHT)

INPUT_CAPS = "udpsrc port=6000 ! " \
        "application/x-rtp,media=video,clock-rate=90000,encoding-name=H264,payload=96 ! " \
        "rtph264depay ! " \
        "avdec_h264 ! " \
        "videoconvert ! " \
        "video/x-raw,format=BGR ! " \
        "appsink drop=1"

def stream():
    app = flask.Flask(__name__)

    @app.route("/")
    def index():
        """The Video streaming home page"""
        return flask.render_template("index.html")

    @app.route("/video_feed")
    def video_feed():
        """The video streaming route"""
        return flask.Response(frame_generator(), mimetype="multipart/x-mixed-replace; boundary=frame")

    def frame_generator():
        """The video streaming generator function"""

        timer = common.Timer()

        while True:
            _, frame = vc.read()

            frame = cv2.resize(frame, VIDEO_SCREEN_SIZE)

            timer.set_time()

            number_of_frames_per_second = int(1 / timer.process_time) 

            cv2.putText(frame, f"FPS: {number_of_frames_per_second}", (10, 30), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, color=(0, 255, 0),thickness=1)

            _, image_buffer = cv2.imencode(".jpg", frame)
            io_buf = io.BytesIO(image_buffer)

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + io_buf.read() + b"\r\n"
            )

    with common.VideoCapture(INPUT_CAPS, cv2.CAP_GSTREAMER) as vc:
        app.run(host="0.0.0.0", threaded=True)


if __name__ == "__main__":
    logging.info("Process started")

    stream()
