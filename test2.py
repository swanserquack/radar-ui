import tkinter as tk
import math
import random

class RadarScan(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Radar Scan")
        self.attributes("-fullscreen", True)  # Make the window fullscreen
        self.configure(bg="black")  # Set the background color

        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.radar_range = 180  # Set the scanning range
        self.scan_interval = 10  # Set the scanning interval in degrees
        self.scan_speed = 1  # Set the scanning speed (larger value for slower scanning)
        self.max_distance = 200  # Maximum distance for detected objects
        self.target_refresh_rate = 1000  # Set the rate at which new targets appear and old targets disappear

        self.draw_radar_arch()
        self.scan_line = self.canvas.create_line(300, 400, 300, 0, fill="green", width=2)
        self.detected_objects = []

        self.scan()

    def draw_radar_arch(self):
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()

        # Increase the radius to extend the radar lines further
        radius = min(window_width, window_height) * 1.7 / 2  # Adjusted to 90% of the minimum dimension
        center_x = window_width / 2
        center_y = window_height

        for angle in range(0, self.radar_range + 1, 10):
            radians = math.radians(angle)
            x = center_x + radius * math.cos(radians)
            y = center_y - radius * math.sin(radians)
            self.canvas.create_line(center_x, center_y, x, y, fill="green", dash=(2, 2))

            # Display distance lines at certain intervals
            if angle % 30 == 0:
                self.canvas.create_text(x, y, text=str(int(angle/30)*10), fill="green")





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

        radius = min(window_width, window_height) * 1.7 / 2  # New radius calculation
        center_x = window_width / 2
        center_y = window_height

        for angle in range(0, self.radar_range + 1, self.scan_interval):
            radians = math.radians(angle)
            x = center_x + radius * math.cos(radians)
            y = center_y - radius * math.sin(radians)
            self.canvas.coords(self.scan_line, center_x, center_y, x, y)
            self.update()

    def detect_objects(self):
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()

        # Simulating detected objects with random distances
        angle = random.randint(0, self.radar_range)
        radius = min(window_width, window_height) * 1.7 / 2  # New radius calculation
        max_distance = int(round(radius * 0.9))  # Convert to integer
        distance = random.randint(0, max_distance)
        if distance < max_distance:
            self.show_detected_object(angle, distance)

    def show_detected_object(self, angle, distance):
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()

        radius = min(window_width, window_height) * 1.7 / 2  # New radius calculation
        center_x = window_width / 2
        center_y = window_height

        radians = math.radians(angle)
        x = center_x + distance * math.cos(radians)
        y = center_y - distance * math.sin(radians)
        detected_object = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")
        self.detected_objects.append(detected_object)

        


    def remove_old_targets(self):
        for target in self.detected_objects:
            if random.random() < 0.05:  # Randomly remove targets
                self.canvas.delete(target)
                self.detected_objects.remove(target)

if __name__ == "__main__":
    app = RadarScan()
    app.mainloop()
