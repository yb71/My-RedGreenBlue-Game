from tkinter import *
from random import randint
from enum import Enum
import time
# from tkinter.ttk import Frame, Label, Style, Button


class Direction(Enum):
    UP = 1; DOWN = 2; LEFT = 3; RIGHT = 4


class Ball:
    def __init__(self, canvas, size):
        self.ball_size = size
        self.canvas = canvas

        color = randint(1, 3)
        if color == 1:
            fill = "blue"
        elif color == 2:
            fill = "red"
        elif color == 3:
            fill = "green"
        else:
            fill = "gray"

        # randomize the starting point
        self.x1 = randint(50, 450)
        self.y1 = randint(50, 450)
        self.x2 = self.x1 + self.ball_size
        self.y2 = self.y1 + self.ball_size
        self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=fill)

        n = randint(1, 4)
        if n == 1:
            self.direction = Direction.UP
        elif n == 2:
            self.direction = Direction.DOWN
        elif n == 3:
            self.direction = Direction.LEFT
        elif n == 4:
            self.direction = Direction.RIGHT

    def move_ball(self):
        global counter
        counter += 1
        delta_x = randint(0, 3)
        delta_y = randint(0, 3)
        d = randint(0, 1)
        if d == 0:
            d = -1

        if self.direction == Direction.DOWN:
            delta_x = d * delta_x  # randomize x direction
        elif self.direction == Direction.UP:
            delta_x = d * delta_x  # randomize x direction
            delta_y = -delta_y
        elif self.direction == Direction.LEFT:
            delta_y = d * delta_y  # randomize y direction
            delta_x = -delta_x
        else: # Direction.RIGHT
            delta_y = d * delta_y  # randomize y direction

        self.canvas.move(self.ball, delta_x, delta_y)  # -------------------------- move the ball
        self.canvas.after(40, self.move_ball)

        if len(canvas.coords(self.ball)) == 0:
            return
        else:
            x1, y1, x2, y2 = canvas.coords(self.ball)

        overlapping_balls = canvas.find_overlapping(x1, y1, x2, y2)  # canvas detects overlapping
        if len(overlapping_balls) > 1 and counter >= 30000:  # half a minute
            canvas.delete(self.ball)
        elif len(overlapping_balls) > 1 and counter < 30000:
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


def update_clock():
    start_time = START_TIME
    diff = int(time.time() - start_time)
    m, s = divmod(diff, 60)
    h, m = divmod(m, 60)
    now = "%d:%02d:%02d" % (h, m, s)
    label.configure(text=now)
    root.after(1000, update_clock)


def count_survivors():
    all_balls = canvas.find_all()
    print(all_balls)
    if len(all_balls) == 1:
        exit()
    root.after(1000, count_survivors)


# ===========================================================================
root = Tk()
root.title('Red-Green-Blue')
root.configure(background="gray")
root.resizable(False, False)
label = Label(text="", width=20, pady=5)
label.pack(side=TOP)
canvas = Canvas(root, bg='white', width=500, height=500)
canvas.pack(side=BOTTOM, padx=5, pady=5)

START_TIME = time.time()
update_clock()

counter = 0
for i in range(50):
    b = Ball(canvas, size=10)
    b.move_ball()


count_survivors()

root.mainloop()
