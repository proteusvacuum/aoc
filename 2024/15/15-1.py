from collections import defaultdict
import sys
import time


with open("input.txt", "r") as f:
    board_input, moves_input = f.read().split("\n\n")

board: dict[tuple[int, int], str] = defaultdict(str)
robot_pos: tuple[int, int] = (-1, -1)

board_lines = board_input.splitlines()
for y, row in enumerate(board_lines):
    for x, item in enumerate(row):
        board[(int(x), int(y))] = item
        if item == "@":
            robot_pos = (int(x), int(y))

MAX_X = len(board_lines)
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
            print(board[(col, row)], end="")
        print("")
    print(move)
    # time.sleep(0.1)
    sys.stdout.flush()

def add_coord(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] + b[0], a[1] + b[1])

# print_board()

checking_pos = robot_pos
for move in moves:
    # Go all the way to an empty space, or a wall
    # print_board(move)
    checking_pos = add_coord(robot_pos, move_to_movement[move])

    if board[checking_pos] == ".":
        # The robot can just move
        board[robot_pos] = "."
        robot_pos = add_coord(robot_pos, move_to_movement[move])
        board[robot_pos] = "@"
        continue

    if board[checking_pos] == "#":
        # This is a wall, do nothing
        continue

    while board[checking_pos] == "O":
        checking_pos = add_coord(checking_pos, move_to_movement[move])
    if board[checking_pos] == "#":
        # a wall, do nothing
        continue
    if board[checking_pos] == ".":
        # replace the first box and the last box
        # this simulates moving all the boxes by one
        # board[robot_pos + move_to_movement[move]] = "."
        board[checking_pos] = "O"
        board[robot_pos] = "."
        robot_pos = add_coord(robot_pos, move_to_movement[move])
        board[robot_pos] = "@"

sum = 0
for pos, item in board.items():
    if item == "O":
        sum += pos[0] + 100 * pos[1]

print(sum)
