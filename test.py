import RPi.GPIO as GPIO
import time

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
step = range(0, StepCount)

step[0] = [0,1,1,1]
step[1] = [0,0,1,1]
step[2] = [1,0,1,1]
step[3] = [1,0,0,1]
step[4] = [1,1,0,1]
step[5] = [1,1,0,0]
step[6] = [1,1,1,0]
step[7] = [0,1,1,0]

GPIO.output(enable_1, 1)
GPIO.output(enable_2, 1)

def setStep(w1, w2, w3, w4):
    GPIO.output(orange, w1)
    GPIO.output(yellow, w2)
    GPIO.output(pink, w3)
    GPIO.output(blue, w4)
 
def forward(delay, steps):
    for i in range(steps):
        for j in range(StepCount):
            setStep(step[j][0], step[j][1], step[j][2], step[j][3])
            time.sleep(delay)
 
def backwards(delay, steps):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep(step[j][0], step[j][1], step[j][2], step[j][3])
            time.sleep(delay)
 
if __name__ == '__main__':
    while True:
        delay = raw_input("Time Delay (ms)?")
        steps = raw_input("How many steps forward? ")
        forward(int(delay) / 1000.0, int(steps))
        steps = raw_input("How many steps backwards? ")
        backwards(int(delay) / 1000.0, int(steps))
 
