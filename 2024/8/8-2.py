from collections import defaultdict
from dataclasses import dataclass
from itertools import permutations
from math import dist

@dataclass
class Coord:
    x: int
    y: int

    def __hash__(self):
        return hash(self.as_tuple())

    def as_tuple(self):
        return (self.x, self.y)


    def distance_from(self, other_coord: "Coord"):
        return dist(self.as_tuple(), other_coord.as_tuple())


with open("input.txt", "r") as f:
    lines = f.read().splitlines()

max_y = len(lines)
max_x = len(lines[0])


def get_antinodes(node_pair) -> list[Coord]:
    node_1 = node_pair[0]
    node_2 = node_pair[1]
    points = []
    for collinear_point in get_collinear_points(node_1, node_2):
        # if (collinear_point.distance_from(node_1) == 2 * collinear_point.distance_from(node_2)) or ((collinear_point.distance_from(node_2) == 2 * collinear_point.distance_from(node_1))):
        points.append(collinear_point)
    return points



def is_collinear(p0: Coord, p1: Coord, p2: Coord):
    x1, y1 = p1.x - p0.x, p1.y - p0.y
    x2, y2 = p2.x - p0.x, p2.y - p0.y
    return abs(x1 * y2 - x2 * y1) < 1e-12


def get_collinear_points(node_1, node_2):
    for x in range(max_x):
        for y in range(max_y):
            if is_collinear(Coord(x, y), node_1, node_2):
                yield Coord(x, y)


nodes = defaultdict(list[Coord])
# freq: (x, y)

for row_num, row in enumerate(lines):
    for column_num, column in enumerate(row):
        if column != ".":
            nodes[column].append(Coord(column_num, row_num))

antinodes = set()
for frequency, coords in nodes.items():
    node_pairs = permutations(coords, r=2)
    for node_pair in node_pairs:
        antinodes |= set(get_antinodes(node_pair))

print(len(antinodes))
