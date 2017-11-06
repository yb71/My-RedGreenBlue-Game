from tkinter import *
from random import randint
from enum import Enum
import time
import csv

WAIT_TIME = 30000  # milliseconds
NUM_OF_BALLS = 100
BALL_SIZE = 10
START_TIME = time.time()
now = time.strftime('%b%d_%Y_%H:%M:%S')
output_file_name = 'data/' + now + '.csv'
run_data = []
ball_objects = {}


class Direction(Enum):
    UP = 1; DOWN = 2; LEFT = 3; RIGHT = 4


class Ball:
    def __init__(self, canvas, ball_objects, size):
        self.ball_size = size
        self.points = 0
        self.canvas = canvas

        # randomize the starting point on  the canvas
        self.x1 = randint(50, 450)
        self.y1 = randint(50, 450)
        self.x2 = self.x1 + self.ball_size
        self.y2 = self.y1 + self.ball_size
        # randomize ball color
        color = randint(1, 3)
        if color == 1:
            self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="blue", tags="blue")
        elif color == 2:
            self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="red", tags="red")
        elif color == 3:
            self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="green", tags="green")
        else:
            self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="gray", tags="gray")

        ball_objects[self.ball] = self  # self.ball is an item id (integer)

        # randomize ball direction
        direct = randint(1, 4)
        if direct == 1:
            self.direction = Direction.UP
        elif direct == 2:
            self.direction = Direction.DOWN
        elif direct == 3:
            self.direction = Direction.LEFT
        elif direct == 4:
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
        my_tag = canvas.itemcget(self.ball, "tags")

        # ------------------------- COLLISION DETECTED -------------------------------------------

        if len(overlapping_balls) > 1 and time_diff >= WAIT_TIME:  # start removing balls
            should_delete = True

            # --------- test output
            # overlap_colors = []
            # for c in overlapping_balls:
            #     overlap_colors.append(canvas.itemcget(c, "tags"))
            # print((self.ball, my_tag, self.points), list(zip(overlapping_balls, overlap_colors)))
            # --------- end of test output

            # count points
            for ob in overlapping_balls:
                if ob == self.ball:
                    continue
                # for any other ball with same color tag, add points
                if canvas.itemcget(ob, "tags") == my_tag:
                    self.points += 1
                    break
                # for any other ball with different color tag, remove points
                else:
                    self.points -= 1

            # if no points lef, delete this ball
            if self.points <= 0:
                # print("deleting")
                canvas.delete(self.ball)
            # if some points left, just bounce
            else:
                self.direction = bounce_off(self.direction)

        elif len(overlapping_balls) > 1 and time_diff < WAIT_TIME:  # only bounce
            for ob in overlapping_balls:
                if ob == self.ball:
                    continue
                # for any other ball with same color tag, add points
                if canvas.itemcget(ob, "tags") == my_tag:
                    self.points += 1
                    break
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


def update_time_label():
    secs = int(time.time() - START_TIME)  # seconds
    mins, secs = divmod(secs, 60)
    hrs, mins = divmod(mins, 60)
    label_text = '{} : {} : {}'.format(hrs, mins, secs)
    label.configure(text=label_text)
    root.after(1000, update_time_label)


def collect_data(run_data):
    total_ball_count = len(canvas.find_all())

    team_red = canvas.find_withtag("red")  # list of ids
    total_red_points = 0
    for red in team_red:
        total_red_points += ball_objects[red].points
    team_red_size = len(team_red)

    team_green = canvas.find_withtag("green")
    total_green_points = 0
    team_green_size = len(team_green)
    for green in team_green:
        total_green_points += ball_objects[green].points

    team_blue = canvas.find_withtag("blue")
    total_blue_points = 0
    team_blue_size = len(team_blue)
    for blue in team_blue:
        total_blue_points += ball_objects[blue].points
    row_of_data = {
        "total count": total_ball_count,
        "red": team_red_size, "total red points": total_red_points,
        "green": team_green_size, "total green points": total_green_points,
        "blue": team_blue_size, "total blue points": total_blue_points
        }
    run_data.append(row_of_data)
    return team_red_size, team_green_size, team_blue_size


def collect_data_before(run_data):
    _, _, _ = collect_data(run_data)
    root.after(1000, collect_data_before, run_data)


def count_survivors(run_data):
    r, g, b = collect_data(run_data)

    # when only one color left, end the game, but first save the data
    if (r != 0 and g == 0 and b == 0) or (r == 0 and g != 0 and b != 0) or (r == 0 and g == 0 and b != 0):
        # saving data to a csv file
        with open(output_file_name, "w") as fh:
            fieldnames = ["total count", "red", "total red points", "green", "total green points", "blue", "total blue points"]
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            for d in run_data:
                writer.writerow(d)
        exit()
    root.after(1000, count_survivors, run_data)


# Main script ===========================================================================
root = Tk()
root.title('Red-Green-Blue Game')
root.configure(background="gray")
root.resizable(False, False)

top_frame = Frame(root, bg="gray")
top_frame.pack(side=TOP)
label = Label(top_frame, text="", width=20, pady=5)
label.pack(side=TOP)
canvas = Canvas(top_frame, bg='white', width=500, height=500)
canvas.pack(side=BOTTOM, padx=5, pady=5)
bottom_frame = Frame(root, bg="gray")
bottom_frame.pack(side=BOTTOM)
lb_red = Label(bottom_frame, text="red", width=10, pady=5, padx=10)
lb_red.pack(side=LEFT)
empty1 = Label(bottom_frame, bg="gray", text="", width=5)
empty1.pack(side=LEFT)
lb_green = Label(bottom_frame, text="green", width=10, pady=5, padx=10)
lb_green.pack(side=LEFT)
empty2 = Label(bottom_frame, bg="gray", text="", width=5)
empty2.pack(side=LEFT)
lb_blue = Label(bottom_frame, text="blue", width=10, pady=5, padx=10)
lb_blue.pack(side=LEFT)

update_time_label()
# create all balls and start moving them
for n in range(NUM_OF_BALLS):
    b = Ball(canvas, ball_objects, size=BALL_SIZE)
    b.move_ball()

collect_data_before(run_data)
count_survivors(run_data)

root.mainloop()
