from flask import Flask, Response
import cv2

app = Flask(__name__)


def generate_frames():
    camera = cv2.VideoCapture(0)
    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    finally:
        camera.release()


@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>Camera Stream</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #000; display: flex; justify-content: center; align-items: center; height: 100vh; }
        img { max-width: 100%; max-height: 100vh; }
    </style>
</head>
<body>
    <img src="/video_feed">
</body>
</html>'''


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
