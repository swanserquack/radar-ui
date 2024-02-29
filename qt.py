import sys
import math
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPen, QColor, QBrush

class RadarScan(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Radar Scan")
        self.setWindowState(Qt.WindowFullScreen)
        self.setStyleSheet("background-color: black;")

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        self.radar_range = 180
        self.scan_interval = 10
        self.scan_speed = 100  # Adjusted for slower scan speed (500 milliseconds)
        self.max_distance = 200
        self.detected_objects = []
        self.scan_angle = 0  # Initial scan angle

        self.draw_radar_arch()
        self.scan_line = self.scene.addLine(300, 400, 300, 0, QPen(Qt.green))

        self.scan_timer = QTimer(self)
        self.scan_timer.timeout.connect(self.scan)
        self.scan_timer.start(self.scan_speed)

    def draw_radar_arch(self):
        window_width = self.width()
        window_height = self.height()
        radius = min(window_width, window_height) * 1.7 / 2
        center_x = window_width / 2
        center_y = window_height

        radar_lines = []
        text_labels = []

        for angle in range(0, self.radar_range + 1, 10):
            radians = math.radians(angle)
            x = center_x + radius * math.cos(radians)
            y = center_y - radius * math.sin(radians)
            line = self.scene.addLine(center_x, center_y, x, y, QPen(Qt.green, 1, Qt.DashLine))
            radar_lines.append(line)
            if angle % 30 == 0:
                text_labels.append(self.scene.addText(str(int(angle/30)*10)))
                text_labels[-1].setPos(x, y)

        self.radar_lines = radar_lines
        self.text_labels = text_labels

    def scan(self):
        self.move_scan_line()
        self.detect_objects()
        self.remove_old_targets()

    def move_scan_line(self):
        window_width = self.width()
        window_height = self.height()
        radius = min(window_width, window_height) * 1.7 / 2
        center_x = window_width / 2
        center_y = window_height

        self.scan_angle += self.scan_interval  # Increment scan angle
        if self.scan_angle > self.radar_range:
            self.scan_angle -= self.radar_range  # Reset scan angle if it exceeds radar range

        radians = math.radians(self.scan_angle)
        self.scan_line.setLine(center_x, center_y, center_x + radius * math.cos(radians), center_y - radius * math.sin(radians))
        self.update()

    def detect_objects(self):
        angle = random.randint(0, self.radar_range)
        max_distance = int(self.max_distance * 4.5)
        distance = random.randint(0, max_distance)
        if distance < max_distance:
            self.show_detected_object(angle, distance)

    def show_detected_object(self, angle, distance):
        window_width = self.width()
        window_height = self.height()
        radius = min(window_width, window_height) * 1.7 / 2
        center_x = window_width / 2
        center_y = window_height
        radians = math.radians(angle)
        x = center_x + distance * math.cos(radians)
        y = center_y - distance * math.sin(radians)
        detected_object = self.scene.addEllipse(x - 5, y - 5, 10, 10, QPen(Qt.red), QBrush(Qt.red))
        self.detected_objects.append(detected_object)

    def remove_old_targets(self):
        targets_to_remove = [target for target in self.detected_objects if random.random() < 0.05]
        for target in targets_to_remove:
            self.scene.removeItem(target)
            self.detected_objects.remove(target)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    radar_scan = RadarScan()
    radar_scan.show()
    sys.exit(app.exec_())
