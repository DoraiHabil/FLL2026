from flask import Flask, Response, request
import queue

app = Flask(__name__)
frame_queue = queue.Queue(maxsize=10)

@app.route("/upload", methods=["POST"])
def upload():
    try:
        frame_queue.put_nowait(request.data)
    except:
        pass
    return "OK"

def generate():
    while True:
        frame = frame_queue.get()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            frame +
            b"\r\n"
        )

@app.route("/video")
def video():
    return Response(
        generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/")
def index():
    return "MJPEG Render Server Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

