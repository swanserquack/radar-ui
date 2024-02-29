import tkinter as tk
import math
import random
import time

class RadarScan(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Radar Scan")
        self.attributes("-fullscreen", True)
        self.configure(bg="black")

        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.radar_range = 180
        self.scan_interval = 10
        self.scan_speed = 1  # Slower scan speed (increased from 1 to 100)
        self.max_distance = 200
        self.detected_objects = []

        self.draw_radar_arch()
        self.scan_line = self.canvas.create_line(300, 400, 300, 0, fill="green", width=2)

        self.scan()

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

    def scan(self):
        while True:
            self.move_scan_line()
            self.detect_objects()
            self.remove_old_targets()
            self.update()
            self.after(self.scan_speed)

    def move_scan_line(self):
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()
        radius = min(window_width, window_height) * 1.7 / 2
        center_x = window_width / 2
        center_y = window_height

        for angle in range(0, self.radar_range + 1, self.scan_interval):
            time.sleep(0.04)
            radians = math.radians(angle)
            x = center_x + radius * math.cos(radians)
            y = center_y - radius * math.sin(radians)
            self.canvas.coords(self.scan_line, center_x, center_y, x, y)
            self.update()

    def detect_objects(self):
        angle = random.randint(0, self.radar_range)
        max_distance = int(self.max_distance * 4.5)
        distance = random.randint(0, max_distance)
        if distance < max_distance:
            self.show_detected_object(angle, distance)

    def show_detected_object(self, angle, distance):
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()
        radius = min(window_width, window_height) * 1.7 / 2
        center_x = window_width / 2
        center_y = window_height
        radians = math.radians(angle)
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
