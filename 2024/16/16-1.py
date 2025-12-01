from collections import deque
from dataclasses import dataclass


with open("test_0.txt", "r") as f:
    lines = f.read().splitlines()

MAX_Y = len(lines)
MAX_X = len(lines[0])


@dataclass
class Coord:
    x: int
    y: int

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other: "Coord") -> bool:
        return self.x == other.x and self.y == other.y

    @property
    def as_tuple(self):
        return (self.x, self.y)


maze: dict[Coord, str] = {}
for row, line in enumerate(lines):
    for column, item in enumerate(line):
        coord = Coord(column, row)
        maze[coord] = item
        if item == "S":
            start = coord
        if item == "E":
            end = coord

SOUTH = Coord(0, 1)
NORTH = Coord(0, -1)
WEST = Coord(-1, 0)
EAST = Coord(1, 0)


def get_accessible_neighbours(graph: dict[Coord, str], node: Coord) -> list[Coord]:
    accessible = []
    for neighbour in [EAST, WEST, NORTH, SOUTH]:
        if graph[node + neighbour] != "#":
            accessible.append(node + neighbour)
    return accessible


def bfs(graph: dict[Coord, str], start: Coord, end: Coord, current_direction: Coord):
    visited_nodes = set([start])
    nodes_to_check = deque([start])
    # Store parent of each node to reconstruct path
    parent: dict[Coord, None | Coord] = {start: None}

    while nodes_to_check:
        current_node = nodes_to_check.popleft()
        if current_node == end:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = parent[current_node]
            return path[::-1]

        for node in get_accessible_neighbours(graph, current_node):
            if node in visited_nodes:
                continue
            visited_nodes.add(node)
            nodes_to_check.append(node)
            parent[node] = current_node

    return None


def calculate_score_from_path(path: list[Coord]):
    score = 0
    current_direction = EAST
    previous_coord = path[0]
    for coord in path[1:]:
        if coord - previous_coord == current_direction:
            score += 1
        else:
            current_direction = coord - previous_coord
            score += 1000
        previous_coord = coord
    return score


path = bfs(maze, start, end, Coord(0, 1))
assert path is not None
# print(len(path))
score = calculate_score_from_path(path)
print(score)

for y in range(MAX_Y):
    for x in range(MAX_X):
        coord = Coord(x, y)
        if coord in path:
            print("X", end="")
        else:
            print(maze[coord], end="")
    print()
