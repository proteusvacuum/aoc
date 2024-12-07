from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import copy
from dataclasses import dataclass
import sys
import time


class LoopException(Exception):
    pass


@dataclass
class Coord:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class Velocity:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


class Board:
    max_x: int
    max_y: int
    obstacles: set[Coord]

    def __init__(self, lines: list[str]):
        self.obstacles = set()
        self.max_x = len(lines)
        self.max_y = len(lines[0])

        for row, line in enumerate(lines):
            for column, char in enumerate(line):
                if char == "#":
                    self.obstacles.add(Coord(x=column, y=row))

    def draw(self, guard: "Guard"):
        sys.stdout.write("\033[H")  # Move cursor to the top-left
        sys.stdout.write("\033[J")  # Clear the screen below the cursor
        for row in range(0, self.max_x):
            for column in range(0, self.max_y):
                if Coord(x=column, y=row) in self.obstacles:
                    print("#", end="")
                elif Coord(x=column, y=row) == guard.position:
                    print(guard.char, end="")
                else:
                    print(".", end="")
            print("\n")
        print(guard.position)
        print(guard.velocity)
        time.sleep(0.1)
        sys.stdout.flush()


class Guard:
    position: Coord
    velocity: Velocity
    board: Board
    visited_position_directions: set[tuple[Coord, Velocity]]

    def __init__(self, lines: list[str], board: Board):
        self.board = board
        for row, line in enumerate(lines):
            for column, char in enumerate(line):
                position = Coord(x=column, y=row)
                if char == "^":
                    self.position = position
                    self.velocity = Velocity(x=0, y=-1)
                if char == ">":
                    self.position = position
                    self.velocity = Velocity(x=1, y=0)
                if char == "<":
                    self.position = position
                    self.velocity = Velocity(x=-1, y=0)
                if char == "v":
                    self.position = position
                    self.velocity = Velocity(x=0, y=1)
        self.visited_position_directions = {(position, self.velocity)}

    @property
    def char(self):
        if self.velocity.x < 0:
            return "<"
        if self.velocity.x > 0:
            return ">"
        if self.velocity.y > 0:
            return "v"
        if self.velocity.y < 0:
            return "^"

    def move(self):
        while self.collision():
            self.rotate()
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        if (self.position, self.velocity) in self.visited_position_directions:
            raise LoopException
        self.visited_position_directions.add((copy(self.position), copy(self.velocity)))
        # self.board.draw(self)

    def rotate(self):
        self.velocity.x, self.velocity.y = -self.velocity.y, self.velocity.x

    def collision(self) -> bool:
        return (
            Coord(
                x=self.position.x + self.velocity.x,
                y=self.position.y + self.velocity.y,
            )
            in self.board.obstacles
        )

    def in_bounds(self):
        return (
            self.position.x > 0
            and self.position.y > 0
            and self.position.x < self.board.max_x
            and self.position.y < self.board.max_y
        )


def get_possible_obstacles(lines):
    # Put new obstacles in any spot that the guard might walk, except the guard's initial position
    board = Board(lines)
    guard = Guard(lines, board)
    initial_position = guard.position
    while guard.in_bounds():
        guard.move()
    visited_positions = set(pos for pos, _ in guard.visited_position_directions)
    return visited_positions - {initial_position}


with open("input.txt", "r") as f:
    lines = f.read().splitlines()


possible_obstacles = get_possible_obstacles(lines)
print("Possible obstacles: ", len(possible_obstacles))
complete = 0
looping_positions = 0


def process_new_obstacle(new_obstacle, lines):
    board = Board(lines)
    board.obstacles.add(Coord(new_obstacle.x, new_obstacle.y))
    guard = Guard(lines, board)
    while guard.in_bounds():
        try:
            guard.move()
        except LoopException:
            return 1, new_obstacle
    return 0, None


with ProcessPoolExecutor() as executor:
    futures = [
        executor.submit(process_new_obstacle, obstacle, lines)
        for obstacle in possible_obstacles
    ]
    for future in as_completed(futures):
        complete += 1
        result, obstacle = future.result()
        looping_positions += result
        print(
            "complete: ",
            complete,
            "/",
            len(possible_obstacles),
            "loops: ",
            looping_positions,
            "looping obstacle",
            obstacle,
        )

print(looping_positions)
