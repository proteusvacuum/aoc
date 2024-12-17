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



robots: list[Robot] = []


for line in lines:
    position = re.findall(r"p=(\d+,\d+)", line)[0].split(",")
    velocity = re.findall(r"v=(-?\d+,-?\d+)", line)[0].split(",")
    robot = Robot(
        (int(position[0]), int(position[1])),
        (int(velocity[0]), int(velocity[1])),
    )
    robots.append(robot)

robot_by_position: dict[tuple, list[Robot]] = defaultdict(list)

for r in robots:
    for i in range(100):
        r.move()
    robot_by_position[r.position].append(r)

mid_row = MAX_Y // 2
mid_col = MAX_X // 2

top_left = [(i, j) for j in range(0, mid_row) for i in range(0, mid_col)]
top_right = [(i, j) for j in range(0, mid_row) for i in range(mid_col + 1, MAX_X)]
bottom_left = [(i, j) for j in range(mid_row + 1, MAX_Y) for i in range(0, mid_col)]
bottom_right = [(i, j) for j in range(mid_row + 1, MAX_Y) for i in range(mid_col + 1, MAX_X)]

quadrant_sums = []
for i, quadrant in enumerate([top_left, top_right, bottom_left, bottom_right]):
    quadrant_sum = 0
    for coord in quadrant:
        quadrant_sum += len(robot_by_position[coord])
        # print(coord, robot_by_position[coord])
    # print("---", quadrant_sum)
    quadrant_sums.append(quadrant_sum)

safety_factor = 1
for quadrant_sum in quadrant_sums:
    safety_factor *= quadrant_sum

print(safety_factor)
