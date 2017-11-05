from tkinter import *
from random import randint
from enum import Enum
import time
import csv

WAIT_TIME = 30000
NUM_OF_BALLS = 100
BALL_SIZE = 10
START_TIME = time.time()


class Direction(Enum):
    UP = 1; DOWN = 2; LEFT = 3; RIGHT = 4


class Ball:
    def __init__(self, canvas, size):
        self.ball_size = size
        self.points = 10
        self.canvas = canvas

        # randomize the starting point
        self.x1 = randint(50, 450)
        self.y1 = randint(50, 450)
        self.x2 = self.x1 + self.ball_size
        self.y2 = self.y1 + self.ball_size

        color = randint(1, 3)
        # self.ball => item id
        if color == 1:
            self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="blue", tags="blue")
        elif color == 2:
            self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="red", tags="red")
        elif color == 3:
            self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="green", tags="green")
        else:
            self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="gray", tags="gray")

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
            delta_x = d * delta_x  # randomize only x direction
        elif self.direction == Direction.UP:
            delta_x = d * delta_x  # randomize only x direction
            delta_y = -delta_y
        elif self.direction == Direction.LEFT:
            delta_y = d * delta_y  # randomize only y direction
            delta_x = -delta_x
        else: # Direction.RIGHT
            delta_y = d * delta_y  # randomize only y direction

        self.canvas.move(self.ball, delta_x, delta_y)  # <<-------------------------- move the ball
        self.canvas.after(40, self.move_ball)

        if len(canvas.coords(self.ball)) == 0:
            return
        else:
            x1, y1, x2, y2 = canvas.coords(self.ball)

        overlapping_balls = canvas.find_overlapping(x1, y1, x2, y2)  # canvas detected overlapping

        time_diff = int((time.time() - START_TIME)*1000)  # milliseconds
        if len(overlapping_balls) > 1 and time_diff >= WAIT_TIME:  # start removing balls
            my_tag = canvas.itemcget(self.ball, "tags")
            should_delete = True

            #--------------------------------------------------------------------
            overlap_colors = []
            for c in overlapping_balls:
                overlap_colors.append(canvas.itemcget(c, "tags"))
            print((self.ball, my_tag), list(zip(overlapping_balls, overlap_colors)))
            #---------------------------------------------------------------------

            for ob in overlapping_balls:
                # if any other ball with same tag, then just bounce, otherwise delete this ball
                if canvas.itemcget(ob, "tags") == my_tag and ob != self.ball:
                    self.direction = bounce_off(self.direction)
                    self.points += 1
                    should_delete = False
                    print("not")
                    break
            if should_delete:  # delete this ball
                print("deleting")
                canvas.delete(self.ball)

        elif len(overlapping_balls) > 1 and time_diff < WAIT_TIME:  # only bounce from other balls
            self.direction = bounce_off(self.direction)

        # bounce off the canvas walls
        if x1 <= 0:
            self.direction = Direction.RIGHT
        elif y1 <= 0:
            self.direction = Direction.DOWN
        elif x2 >= 500:
            self.direction = Direction.LEFT
        elif y2 >= 500:
            self.direction = Direction.UP


def bounce_off(start_direction):
    if start_direction == Direction.DOWN:
        end_direction = Direction.UP
    elif start_direction == Direction.UP:
        end_direction = Direction.DOWN
    elif start_direction == Direction.LEFT:
        end_direction = Direction.RIGHT
    elif start_direction == Direction.RIGHT:
        end_direction = Direction.LEFT
    else:
        end_direction = start_direction
    return end_direction


def update_label():

    root.after(1000, update_label)


# def update_clock():
#     start_time = START_TIME
#     diff = int(time.time() - start_time)
#     m, s = divmod(diff, 60)
#     h, m = divmod(m, 60)
#     now = "%d:%02d:%02d" % (h, m, s)
#     label.configure(text=now)
#     root.after(1000, update_clock)


def count_survivors(t, run_data):
    now = time.strftime('%b%d_%Y_%H:%M:%S')
    # time_now = time.strftime('%H:%M:%S')

    all_balls = canvas.find_all()
    total_ball_count = len(all_balls)

    team_red = len(canvas.find_withtag("red"))
    team_green = len(canvas.find_withtag("green"))
    team_blue = len(canvas.find_withtag("blue"))

    data = {"t": t, "total count": total_ball_count, "red": team_red, "green": team_green, "blue": team_blue}
    # print(data)
    t += 1
    run_data.append(data)

    if (team_red != 0 and team_blue == 0 and team_green == 0) \
            or (team_red == 0 and team_blue != 0 and team_green == 0) \
            or (team_red == 0 and team_blue == 0 and team_green != 0):
        file_name = 'data/' + now + '.csv'
        with open(file_name, "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for d in run_data:
                line = d["t"], d["total count"], d["red"], d["green"], d["blue"]
                writer.writerow(line)
        exit()
    root.after(1000, count_survivors, t, run_data)


# Main script ===========================================================================
root = Tk()
root.title('Red-Green-Blue')
root.configure(background="gray")
root.resizable(False, False)
label = Label(text="", width=20, pady=5)
label.pack(side=TOP)
canvas = Canvas(root, bg='white', width=500, height=500)
canvas.pack(side=BOTTOM, padx=5, pady=5)

# update_clock()
update_label()


for n in range(NUM_OF_BALLS):
    b = Ball(canvas, size=BALL_SIZE)
    b.move_ball()

t = 1
run_data = []
count_survivors(t, run_data)

root.mainloop()
