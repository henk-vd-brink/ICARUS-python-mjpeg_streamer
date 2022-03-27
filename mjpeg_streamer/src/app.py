import multiprocessing
import flask
import cv2
import io
import os

from . import common

import logging
logging.basicConfig(level=logging.DEBUG)


VIDEO_SCREEN_WIDTH = 640
VIDEO_SCREEN_HEIGHT = 480
UDPSRC_PORT = 6000

INPUT_CAPS = f"udpsrc port={UDPSRC_PORT} !\
            application/x-rtp,media=video,encoding-name=H264 !\
            queue !\
            rtpjitterbuffer latency=100 !\
            rtph264depay !\
            h264parse !\
            avdec_h264 !\
            videoconvert !\
            video/x-raw,format=BGR !\
            queue !\
            appsink drop=1"


def stream(queue_s2d, queue_d2s):
    app = Flask(__name__)

    @app.route("/")
    def index():
        """The Video streaming home page."""
        return render_template("index.html")

    @app.route("/video_feed")
    def video_feed():
        """Video streaming route. Put this in the src attribute of an img tag."""
        return Response(frame_generator(), mimetype="multipart/x-mixed-replace; boundary=frame")

    def frame_generator():
        """Video streaming generator function."""

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

    with VideoCapture(INPUT_CAPS, cv2.CAP_GSTREAMER) as vc:
        app.run(host="0.0.0.0", threaded=True)


if __name__ == "__main__":
    process_stream = mp.Process(target=stream)
    process_stream.start()
