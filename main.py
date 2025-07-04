from flask import Flask, Response
import cv2
import mediapipe as mp
import numpy as np
import serial
import time


url = 'http://192.168.252.177:81/stream'


try:
    arduino = serial.Serial('COM3', 9600)  
    time.sleep(2)
    print("Conectado al Arduino por COM3")
except:
    arduino = None
    print("No se pudo conectar al Arduino por COM")

app = Flask(__name__)

# Inicializar MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Función para calcular ángulo 
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    ab = b - a
    bc = c - b
    radians = np.arctan2(bc[1], bc[0]) - np.arctan2(ab[1], ab[0])
    return int(np.abs(np.degrees(radians)) % 360)


def gen_frames():
    cap = cv2.VideoCapture(url)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark

            cuello = (lm[0].x * w, lm[0].y * h)
            hi = (lm[11].x * w, lm[11].y * h)
            ci = (lm[13].x * w, lm[13].y * h)
            mi = (lm[15].x * w, lm[15].y * h)
            hd = (lm[12].x * w, lm[12].y * h)
            cd = (lm[14].x * w, lm[14].y * h)
            md = (lm[16].x * w, lm[16].y * h)

            ang_cuello = 90  # puedes usar otro cálculo si deseas
            ang_hi = calculate_angle(hi, ci, mi)
            ang_hd = calculate_angle(hd, cd, md)
            ang_ci = ang_hi
            ang_cd = ang_hd

            # Enviar ángulos por serial si está conectado
            if arduino:
                cadena = f"{ang_cuello},{ang_hi},{ang_hd},{ang_ci},{ang_cd}\n"
                arduino.write(cadena.encode('utf-8'))

            # Dibujar el esqueleto
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Redimensionar para mejor vista
        frame = cv2.resize(frame, (960, 720))

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Página principal
@app.route('/')
def index():
    return '''
    <html>
    <head><title>Imitación en Vivo</title></head>
    <body style="text-align:center; background:#111; color:white;">
        <h1>Imitación en Vivo</h1>
        <img src="/video_feed" width="960" height="720" style="border: 4px solid white; border-radius: 10px;">
    </body>
    </html>
    '''

# Ruta del video
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Iniciar servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
