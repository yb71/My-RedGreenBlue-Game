from tkinter import *
from random import randint
from math import sqrt
from enum import Enum
# from tkinter.ttk import Frame, Label, Style, Button


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Ball:
    def __init__(self, canvas, size, fill="gray"):
        self.ball_size = size
        self.canvas = canvas
        if fill == "blue":
            self.color = "blue"
        elif fill == "red":
            self.color = "red"
        else:
            self.color = "gray"

        # randomize the starting point
        self.x1 = randint(50, 450)
        self.y1 = randint(50, 450)
        self.x2 = self.x1 + self.ball_size
        self.y2 = self.y1 + self.ball_size
        self.radius = int(distance_between_two_points(self.x1, self.y1, self.x2, self.y2)/2)
        self.center_x = self.x1 + int(self.ball_size / 2)
        self.center_y = self.y1 + int(self.ball_size / 2)
        self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=fill, tags="ball")
        self.direction = Direction.DOWN

    def move_ball(self):
        delta_x = randint(0, 4)
        delta_y = randint(0, 4)
        d = randint(0, 1)
        if d == 0:
            d = -1

        if self.direction == Direction.DOWN:
            delta_x = d * delta_x
        elif self.direction == Direction.UP:
            delta_x = d * delta_x
            delta_y = -delta_y
        elif self.direction == Direction.LEFT:
            delta_y = d * delta_y
            delta_x = -delta_x
        else: # Direction.RIGHT
            delta_y = d * delta_y

        self.canvas.move(self.ball, delta_x, delta_y)
        self.canvas.after(50, self.move_ball)

        x1, y1, x2, y2 = canvas.coords(self.ball)



        overlapping_balls = canvas.find_overlapping(x1-2, y1-2, x2+2, y2+2) # canvas detects overlapping
        if len(overlapping_balls) > 1:
            if self.direction == Direction.DOWN:
                self.direction = Direction.UP
            elif self.direction == Direction.UP:
                self.direction = Direction.DOWN
            elif self.direction == Direction.LEFT:
                self.direction = Direction.RIGHT
            elif self.direction == Direction.RIGHT:
                self.direction = Direction.LEFT

        # if hit the canvas walls
        if x1 <= 0:
            self.direction = Direction.RIGHT
        elif y1 <= 0:
            self.direction = Direction.DOWN
        elif x2 >= 500:
            self.direction = Direction.LEFT
        elif y2 >= 500:
            self.direction = Direction.UP




def distance_between_two_points(x1, y1, x2, y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)


root = Tk()
root.title('My window title')
root.configure(background="gray")
root.resizable(False, False)
canvas = Canvas(root, bg='white', width=500, height=500)
canvas.pack(side=LEFT, padx=5, pady=5)

ball1 = Ball(canvas, size=12, fill="blue")
ball1.move_ball()
ball2 = Ball(canvas, size=12, fill="red")
ball2.move_ball()

for i in range(50):
    b = Ball(canvas, size=10)
    b.move_ball()

root.mainloop()


