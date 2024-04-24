import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
import cv2
from ultralytics import YOLO

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Детекция номерных знаков")
        self.setGeometry(100, 100, 800, 600)

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)

        self.open_button = QPushButton("Открыть видео")
        self.open_button.clicked.connect(self.open_video)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.open_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)

        self.cap = None
        self.model = None

    def open_video(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Выбрать видео", "", "Video Files (*.mp4 *.avi)")
        if filename:
            self.cap = cv2.VideoCapture(filename)
            if not self.cap.isOpened():
                print("Ошибка при открытии файла")
                return
            self.timer.start(33)

            self.model = YOLO("best.pt")

    def next_frame(self):
        ret, frame = self.cap.read()
        if ret:
            results = self.model(frame)

            for box in results[0].boxes.data:
                x1, y1, x2, y2, score, label = box
                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                text = "number plates"
                cv2.putText(frame, f'{score:.2f} {text}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            q_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.timer.stop()
            self.cap.release()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())

