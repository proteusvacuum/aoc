from dataclasses import dataclass
from collections import defaultdict
import sys
import time
from typing import Self


with open("test_0.txt", "r") as f:
    board_input, moves_input = f.read().split("\n\n")

@dataclass
class Box:
    left_coord: tuple[int, int]
    right_coord: tuple[int, int]

    def __hash__(self) -> int:
        return hash(self.left_coord + self.right_coord)

    def coord_tuple(self):
        return (self.left_coord, self.right_coord)

    def char(self, pos) -> str:
        if pos == self.left_coord:
            return "["
        return "]"

    def move(self, movement) -> None:
        self.left_coord, self.right_coord = self._add_coord(movement)

    def _add_coord(self, movement):
        new_left = (self.left_coord[0] + movement[0], self.left_coord[1] + movement[1])
        new_right = (self.right_coord[0] + movement[0], self.right_coord[1] + movement[1])
        return new_left, new_right

    def is_touching(self, board, movement) -> list[Self]:
        boxes = set()
        left_side = add_coord(self.left_coord, movement)
        right_side = add_coord(self.right_coord, movement)
        if isinstance(board[left_side], Box) and board[left_side] != self:
            boxes.add(board[left_side])
        if isinstance(board[right_side], Box) and board[right_side] != self:
            boxes.add(board[right_side])
        return list(boxes)


board: dict[tuple[int, int], str | Box] = defaultdict(str)
robot_pos: tuple[int, int] = (-1, -1)

board_lines = board_input.splitlines()
for y, row in enumerate(board_lines):
    for x in range(0, len(row) * 2, 2):
        item = row[x // 2]
    # for x, item in enumerate(row):
        if item == "O":
            box = Box((int(x), int(y)), (int(x+1), int(y)))
            board[(int(x), int(y))] = box
            board[(int(x+1), int(y))] = box
        elif item == "@":
            board[(int(x), int(y))] = "@"
            robot_pos = (int(x), int(y))
            board[(int(x+1), int(y))] = "."
        else:
            board[(int(x), int(y))] = item
            board[(int(x+1), int(y))] = item


MAX_X = len(board_lines * 2)
MAX_Y = len(board_lines[0])

moves = [move for move in moves_input if move != "\n"]
move_to_movement = {
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
    ">": (1, 0),
}

def print_board(move=""):
    sys.stdout.write("\033[H")  # Move cursor to the top-left
    sys.stdout.write("\033[J")  # Clear the screen below the cursor
    for row in range(0, MAX_Y):
        for col in range(0, MAX_X):
            item = board[(col, row)]
            if isinstance(item, Box):
                print(item.char((col, row)), end="")
            else:
                print(item, end="")
        print("")
    print(move)
    time.sleep(0.5)
    sys.stdout.flush()

def add_coord(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] + b[0], a[1] + b[1])


checking_pos = robot_pos
for i, move in enumerate(moves):
    # Go all the way to an empty space, or a wall
    print_board(move)
    movement = move_to_movement[move]


print_board(move)
sum = 0
for pos, item in board.items():
    if item == "O":
        sum += pos[0] + 100 * pos[1]

print(sum)
