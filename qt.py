import sys
import math
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsTextItem, QGraphicsEllipseItem
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPen, QColor, QPolygonF, QBrush
from gpiozero import DistanceSensor

sensor = DistanceSensor(echo=9, trigger=10)


class RadarScan(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Radar Scan")
        self.setStyleSheet("background-color: black;")

        # Determine the screen dimensions
        screen_geo = QApplication.primaryScreen().geometry()
        self.screen_width = screen_geo.width()
        self.screen_height = screen_geo.height()

        # Adjust scene and view dimensions accordingly
        self.scene = QGraphicsScene(0, 0, self.screen_width, self.screen_height)
        self.view = QGraphicsView(self.scene)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setCentralWidget(self.view)

        # Initialize radar scan parameters
        self.mode = "RWS"
        self.text_item = QGraphicsTextItem("RWS")
        self.text_item.setDefaultTextColor(Qt.green)
        self.text_item.setPos(0,0)
        self.scene.addItem(self.text_item)

        self.radar_range = 180
        self.min_radar = 0
        self.scan_interval = 1
        self.intersection_distance = -207  # Adjust this value as needed
        self.scan_speed = 50  # Adjusted for slower scan speed (500 milliseconds)
        self.direction = 1  # Initialize direction of movement to forward
        self.max_distance = min(self.screen_width, self.screen_height) * 0.7
        self.detected_objects = []
        self.scan_angle = 0  # Initial scan angle
        self.center_x = self.screen_width / 2
        self.center_y = self.screen_height

        self.draw_radar_arch()

        # Draw the radar scan line
        self.scan_line = self.scene.addLine(self.screen_width / 2, self.screen_height, self.screen_width / 2, 0, QPen(Qt.green))

        for i in range(80,100):
            distance = random.randint(200, int(self.max_distance))
            if distance < self.max_distance:
                angle = i
                radians = math.radians(angle)
                x = self.center_x + distance * math.cos(radians)
                y = self.center_y - distance * math.sin(radians)
                detected_object = self.scene.addEllipse(x - 5, y - 5, 10, 10, Qt.red, Qt.red)
                self.detected_objects.append({"object": detected_object, "x": x, "y": y, "angle": angle})
                self.draw_lines_between_adjacent_points()
        # Start the scan timer
        self.scan_timer = QTimer(self)
        self.scan_timer.timeout.connect(self.scan)
        self.scan_timer.start(self.scan_speed)

    def draw_radar_arch(self):

        radar_lines = []

        # Calculate the maximum radius that ensures the lines cover the entire screen height
        max_radius = min(self.center_x, self.center_y)

        for angle in range(0, self.radar_range + 1, 10):
            radians = math.radians(angle)
            x = self.center_x + max_radius * math.cos(radians)
            y = self.center_y - max_radius * math.sin(radians)
            line = self.scene.addLine(self.center_x, self.center_y, x, y, QPen(Qt.green, 1, Qt.DashLine))
            radar_lines.append(line)

        self.radar_lines = radar_lines

    def scan(self):
        self.move_scan_line()
        # self.distance_and_plot()
        self.check_mode_and_change()
        self.detect_objects()
        #self.remove_old_targets()

    def move_scan_line(self):
        # Declare once initially if really need performance
        window_width = self.width()
        window_height = self.height()
        radius = min(window_width, window_height) * 1.7 / 2
        
        if self.mode == "RWS":
            self.radar_range = 180
            self.min_radar = 0
        elif self.mode == "STT":
            angle = self.detected_objects[0]["angle"]
            self.radar_range = angle + 15
            self.min_radar = angle - 15
        elif self.mode == "TWS":
            angles = [obj["angle"] for obj in self.detected_objects]
            max_angle = max(angles)
            min_angle = min(angles)
            self.radar_range = max_angle + 15
            self.min_radar = min_angle - 15
            if self.radar_range > 180:
                self.radar_range = 180
            if self.min_radar < 0:
                self.min_radar = 0

        self.scan_angle += self.direction * self.scan_interval  # Increment scan angle based on direction
        if self.scan_angle > self.radar_range:
            self.direction = -1  # Change direction to backward
            self.scan_angle = self.radar_range - (self.scan_angle - self.radar_range)
        elif self.scan_angle < self.min_radar:
            self.direction = 1  # Change direction to forward
            self.scan_angle = abs(self.scan_angle)

        radians = math.radians(self.scan_angle)
        self.scan_line.setLine(self.center_x, self.center_y, self.center_x + radius * math.cos(radians), self.center_y - radius * math.sin(radians))
        self.update()


    def distance_and_plot(self):
        distance = sensor.distance * 100

    def check_mode_and_change(self):
        number_of_objects = len(self.detected_objects)
        if number_of_objects == 0 and self.mode != "RWS":
            self.mode = "RWS"
            self.text_item.setPlainText("RWS")
        elif number_of_objects == 1 and self.mode != "STT":
            self.mode = "STT"
            self.text_item.setPlainText("STT")
        elif number_of_objects > 1 and self.mode != "TWS":
            self.mode = "TWS"
            self.text_item.setPlainText("TWS")


    def detect_objects(self):
        distance = random.randint(0, int(self.max_distance))
        if distance < self.max_distance and (len(self.detected_objects) == 0 or len(self.detected_objects) == 1):
            angle = random.randint(0, self.radar_range)
            self.show_detected_object(angle, distance)
            self.draw_lines_between_adjacent_points()

    def show_detected_object(self, angle, distance):
        radians = math.radians(angle)
        x = self.center_x + distance * math.cos(radians)
        y = self.center_y - distance * math.sin(radians)
        detected_object = self.scene.addEllipse(x - 5, y - 5, 10, 10, Qt.red, Qt.red)
        self.detected_objects.append({"object": detected_object, "x": x, "y": y, "angle": angle})

    def remove_old_targets(self):
        targets_to_remove = [target for target in self.detected_objects if random.random() < 0.05]
        for target in targets_to_remove:
            self.scene.removeItem(target["object"])
            self.detected_objects.remove(target)
    
    def draw_lines_between_adjacent_points(self):
        # Sort detected objects by angle
        sorted_objects = sorted(self.detected_objects, key=lambda obj: obj['angle'])

        # Iterate through sorted list to find adjacent points
        for i in range(len(sorted_objects) - 1):
            current_angle = sorted_objects[i]['angle']
            next_angle = sorted_objects[i + 1]['angle']

            # Check if the difference between adjacent angles is within a threshold
            angle_threshold = 1  # Adjust this threshold as needed
            if abs(next_angle - current_angle) <= angle_threshold:
                # Found adjacent angles, draw a line between them
                self.draw_filled_line_between_points(sorted_objects[i], sorted_objects[i + 1])

    def draw_filled_line_between_points(self, point1, point2):
        # Draw filled line between two points
        polygon = QPolygonF()
        x1, y1 = point1['x'], point1['y']
        x2, y2 = point2['x'], point2['y']
        
        # Calculate intersection points with the radar arch
        intersection_point1 = self.calculate_intersection_point(x1, y1, self.center_x, self.center_y)
        intersection_point2 = self.calculate_intersection_point(x2, y2, self.center_x, self.center_y)
        
        # Add points to the polygon
        polygon.append(QPointF(x1, y1))
        polygon.append(intersection_point1)
        polygon.append(intersection_point2)
        polygon.append(QPointF(x2, y2))
        
        # Add polygon to scene
        filled_line = self.scene.addPolygon(polygon, QPen(Qt.red), QBrush(Qt.red))

    def calculate_intersection_point(self, x, y, center_x, center_y):
        # Calculate intersection point with the radar arch
        angle = math.atan2(y - center_y, x - center_x)
        intersection_x = center_x + (self.max_distance - self.intersection_distance) * math.cos(angle)
        intersection_y = center_y + (self.max_distance - self.intersection_distance) * math.sin(angle)
        return QPointF(intersection_x, intersection_y)

    def draw_line_between_points(self, point1, point2):
        # Draw line between two points
        line = self.scene.addLine(point1['x'], point1['y'], point2['x'], point2['y'], QPen(Qt.red))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    radar_scan = RadarScan()
    radar_scan.showFullScreen()
    sys.exit(app.exec_())
