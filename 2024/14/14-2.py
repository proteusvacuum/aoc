import sys
import time
from collections import defaultdict
from dataclasses import dataclass
import re

# with open("test_1.txt", "r") as f:
#     lines = f.read().splitlines()
# MAX_X = 11
# MAX_Y = 7

with open("input.txt", "r") as f:
    lines = f.read().splitlines()
MAX_X = 101
MAX_Y = 103

@dataclass
class Robot:
    position: tuple[int, int]
    velocity: tuple[int, int]

    def move(self):
        new_x = (self.position[0] + self.velocity[0]) % MAX_X
        new_y = (self.position[1] + self.velocity[1]) % MAX_Y
        self.position = (new_x, new_y)

robot_by_position: dict[tuple, list[Robot]] = defaultdict(list)

robots: list[Robot] = []


def print_board():
    sys.stdout.write("\033[H")  # Move cursor to the top-left
    sys.stdout.write("\033[J")  # Clear the screen below the cursor
    for row in range(0, MAX_Y):
        for col in range(0, MAX_X):
            print(len(robot_by_position[(col, row)]), end="")
        print("")
    # time.sleep(0.1)
    sys.stdout.flush()

for line in lines:
    position = re.findall(r"p=(\d+,\d+)", line)[0].split(",")
    velocity = re.findall(r"v=(-?\d+,-?\d+)", line)[0].split(",")
    robot = Robot(
        (int(position[0]), int(position[1])),
        (int(velocity[0]), int(velocity[1])),
    )
    robots.append(robot)
    robot_by_position[robot.position].append(robot)

mid_row = MAX_Y // 2
mid_col = MAX_X // 2


def count_adjacents(robot: Robot) -> tuple[int, int]:
    # How many robots are beside this one?
    count_left = 0
    x = robot.position[0]
    while x >= 0:
        x -= 1
        if len(robot_by_position[(x, robot.position[1])]):
            count_left += 1
        else:
            break
    count_right = 0
    x = robot.position[0]
    while x < MAX_X:
        x += 1
        if len(robot_by_position[(x, robot.position[1])]):
            count_right += 1
        else:
            break
    return (count_left, count_right)

print_board()
# A tree has 1, then 3, then 5, then 7 items
# O(n^2)
tick_num = 0
def tick():
    robot_by_position.clear()
    for r in robots:
        r.move()
        robot_by_position[r.position].append(r)
    global tick_num
    tick_num += 1
    # print_board()

while not all(len(rs) <= 1 for rs in robot_by_position.values()):
    tick()
print_board()
breakpoint()


while True:
    start_robots = [robot for robot in robots if count_adjacents(robot) == (0, 0)]  # Single robot
    for robot in start_robots:
        checking_robot = robot
        adjacents = 0
        # Move down
        while checking_robot is not None:
            down_robots = robot_by_position[checking_robot.position[0], checking_robot.position[1]]
            if down_robots:
                checking_robot = down_robots[0]
                down_adjacents = count_adjacents(checking_robot)
                if down_adjacents is not None and down_adjacents == (adjacents + 1, adjacents + 1):
                    adjacents += 1
                else:
                    checking_robot = None
            if adjacents > 0:
                print_board()
                breakpoint()
    tick()
