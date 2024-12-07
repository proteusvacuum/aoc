from dataclasses import dataclass
import sys
import time


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
        time.sleep(0.2)
        sys.stdout.flush()


class Guard:
    position: Coord
    velocity: Velocity
    board: Board
    visited_positions: set[Coord] = set()

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
        if self.collision():
            self.rotate()
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        self.visited_positions.add(self.position)
        # self.board.draw(self)

    def rotate(self):
        self.velocity.x, self.velocity.y = -self.velocity.y, self.velocity.x

    def collision(self):
        return (
            Coord(
                x=(self.position.x + self.velocity.x),
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


with open("input.txt", "r") as f:
    lines = f.read().splitlines()

guard = Guard(lines, Board(lines))
while guard.in_bounds():
    guard.move()

print(len(guard.visited_positions))
