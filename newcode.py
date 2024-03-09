import tkinter as tk
import math
import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor
from threading import Thread
import random

enable_1 = 7
enable_2 = 40
orange = 3
yellow = 38
pink = 5
blue = 12

GPIO.setmode(GPIO.BOARD)

GPIO.setup(orange, GPIO.OUT)
GPIO.setup(pink, GPIO.OUT)
GPIO.setup(enable_1, GPIO.OUT)
GPIO.setup(enable_2, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

StepCount = 8
step = [
    [0, 1, 1, 1],
    [0, 0, 1, 1],
    [1, 0, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 0, 1],
    [1, 1, 0, 0],
    [1, 1, 1, 0],
    [0, 1, 1, 0]
]

GPIO.output(enable_1, 1)
GPIO.output(enable_2, 1)

sensor = DistanceSensor(echo=9, trigger=10)

def setStep(w1, w2, w3, w4):
    GPIO.output(orange, w1)
    GPIO.output(yellow, w2)
    GPIO.output(pink, w3)
    GPIO.output(blue, w4)

def forward(delay, steps):
    for _ in range(steps):
        for j in range(StepCount):
            setStep(step[j][0], step[j][1], step[j][2], step[j][3])
            time.sleep(delay)

def move_motor():
    while True:
        forward(int(10) / 1000.0, 1)  # Move one step
        time.sleep(0.01)

class RadarScan(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Radar Scan")
        self.attributes("-fullscreen", True)
        self.configure(bg="black")

        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.radar_range = 180
        self.scan_speed = 20  # Adjusted scan speed
        self.max_distance = 100  # Adjusted max distance to 1 meter
        self.detected_objects = []

        self.draw_radar_arch()
        self.scan_line = self.canvas.create_line(300, 400, 300, 0, fill="green", width=2)

        self.move_motor_thread = Thread(target=move_motor)
        self.move_motor_thread.daemon = True
        self.move_motor_thread.start()

        self.scan(angle=0)

    def draw_radar_arch(self):
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()
        radius = min(window_width, window_height) * 1.7 / 2
        center_x = window_width / 2
        center_y = window_height

        radar_lines = []
        text_labels = []

        for angle in range(0, self.radar_range + 1, 10):
            radians = math.radians(angle)
            x = center_x + radius * math.cos(radians)
            y = center_y - radius * math.sin(radians)
            radar_lines.append(self.canvas.create_line(center_x, center_y, x, y, fill="green", dash=(2, 2)))
            if angle % 30 == 0:
                text_labels.append(self.canvas.create_text(x, y, text=str(int(angle/30)*10), fill="green"))

        self.radar_lines = radar_lines
        self.text_labels = text_labels

    def scan(self, angle):
        radians = math.radians(angle)
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()
        radius = min(window_width, window_height) * 1.7 / 2
        center_x = window_width / 2
        center_y = window_height

        x = center_x + radius * math.cos(radians)
        y = center_y - radius * math.sin(radians)
        self.canvas.coords(self.scan_line, center_x, center_y, x, y)

        self.detect_objects(angle)  # Detect objects at this angle

        if angle < 180:
            self.after(self.scan_speed, self.scan, angle + 3)  # Increment by 3 degrees
        else:
            self.after(self.scan_speed, self.scan, 0)  # Restart scan from 0 angle

    def detect_objects(self, angle):
        distance = sensor.distance * 100  # Convert to centimeters
        if distance != 100:  # Display object if not 1 meter away
            self.show_detected_object(angle, distance)
        else:
            self.remove_old_targets()

    def show_detected_object(self, angle, distance):
        radians = math.radians(angle)
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()
        radius = min(window_width, window_height) * 1.7 / 2
        center_x = window_width / 2
        center_y = window_height
        x = center_x + distance * math.cos(radians)
        y = center_y - distance * math.sin(radians)
        detected_object = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")
        self.detected_objects.append(detected_object)

    def remove_old_targets(self):
        targets_to_remove = [target for target in self.detected_objects if random.random() < 0.05]
        for target in targets_to_remove:
            self.canvas.delete(target)
            self.detected_objects.remove(target)

if __name__ == "__main__":
    app = RadarScan()
    app.mainloop()
