from tkinter import *
from random import randint
from enum import Enum
# from tkinter.ttk import Frame, Label, Style, Button

START = False


class Direction(Enum):
    UP = 1; DOWN = 2; LEFT = 3; RIGHT = 4


class Ball:
    def __init__(self, canvas, size, fill="gray"):
        self.ball_size = size
        self.canvas = canvas

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

        self.canvas.move(self.ball, delta_x, delta_y)
        self.canvas.after(40, self.move_ball)

        if len(canvas.coords(self.ball)) == 0:
            return
        else:
            x1, y1, x2, y2 = canvas.coords(self.ball)

        overlapping_balls = canvas.find_overlapping(x1, y1, x2, y2)  # canvas detects overlapping
        if len(overlapping_balls) > 1:
            if START:
                canvas.delete(self.ball)
            else:
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


def callback():
    START = True


root = Tk()
root.title('My window title')
root.configure(background="gray")
root.resizable(False, False)
canvas = Canvas(root, bg='white', width=500, height=500)
canvas.pack(side=TOP, padx=5, pady=5)
button = Button(root, text="Start", width=20, pady=5, command=callback)
button.pack(side=BOTTOM)

for i in range(50):
    b = Ball(canvas, size=10)
    b.move_ball()

root.mainloop()


# center_x = self.x1 + int(self.ball_size / 2)
# center_y = self.y1 + int(self.ball_size / 2)
# item = canvas.find_closest(center_x, center_y)[0]
# print(item)

# canvas.itemconfig(self.ball, fill="red")