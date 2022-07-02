import Adafruit_PCA9685
from time import sleep
from random import randint
from numpy import abs


class Tracker:
    def __init__(self, size=(640, 480)):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)

        self.angle_up_record = 90               # start at center(90, 90) degree
        self.angle_down_record = 90
        self.set_two_angle(90, 90)
        sleep(0.5)

        self.acceptable_x = size[0] * 0.3 / 2   # if in this area, cam won't move, the area is a rectangle
        self.acceptable_y = size[1] * 0.3 / 2

        self.center_x = size[0] / 2             # the picture's center
        self.center_y = size[1] / 2

    def track(self, x, y):
        """input x and Y, the cam will set its angels to remain the x and Y in the center of the picture"""
        move_x = self.center_x - x
        move_y = self.center_y - y

        degree_x = int(move_x / 8)      # degrees which should be rotated
        degree_y = int(move_y / 8)

        if abs(move_x) > self.acceptable_x:     # rotate down cam
            self.angle_down_record += degree_x
            if self.angle_down_record < 0:
                self.angle_down_record = 0
            elif self.angle_down_record > 180:
                self.angle_down_record = 180
            self.set_servo_angle("down", self.angle_down_record)

        if abs(move_y) > self.acceptable_y:     # rotate up cam
            self.angle_up_record += degree_y
            if self.angle_up_record < 0:
                self.angle_up_record = 0
            elif self.angle_up_record > 180:
                self.angle_up_record = 180
            self.set_servo_angle("up", self.angle_up_record)

        sleep(0.25)      # up to how fast the detecting network works

    def set_servo_angle(self, position, angle):
        """input the position and an angle, it will autotransform it to pwm"""
        if position == "up":
            self.angle_up_record = angle
            channel = 4
        elif position == "down":
            self.angle_down_record = angle
            channel = 0
        else:
            print("position only includes 'up' and 'down'")
            raise KeyError

        date = int(4096 * ((angle * 11) + 500) / 20000)
        self.pwm.set_pwm(channel, 0, date)

    def random_patrol(self, interval=5):
        """start to rotate random angles per interval"""
        self.angle_up_record = randint(0, 180)  # set random degrees
        self.angle_down_record = randint(0, 180)

        self.set_two_angle(self.angle_up_record, self.angle_down_record)
        sleep(interval)

    def set_two_angle(self, angle_up, angle_down):
        """set tow angle at the same time"""
        self.angle_up_record = angle_up         # record the angles
        self.angle_down_record = angle_down

        self.set_servo_angle("up", angle_up)
        self.set_servo_angle("down", angle_down)

    def unlock_cam(self):
        """make the cam totates freely"""
        self.pwm.set_pwm(0, 0, 0)
        self.pwm.set_pwm(4, 0, 0)


if __name__ == "__main__":
    demo = Tracker(size=(640, 480))       # auto set to center(90, 90) degree

    demo.unlock_cam()
    demo.track(30, 50)                    # input x, y

    while True:
        demo.random_patrol()              # start to patrol
