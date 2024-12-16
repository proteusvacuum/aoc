import re

# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400

# 94A + 22B = 8400
# 34A + 67B = 5400

# B = (8400 - 94A)/22
# 34A + 67(8400 - 94A)/22 = 5400
# 34A + (67*8400/22) - (67*94/22)A= 5400
# (34 - 67*94/22)A = 5400 - (67*8400/22)
# A = (5400 - (67*8400/22))/ (34 - 67*94/22)

# A = (8400 - 22B) / 94
# 34(8400 - 22B) + 67B = 5400
# 34*8400 - 34*22B + 67B = 5400
# (34*22 + 67)B = 5400 - 34*8400

# B = (5400 - 34*8400)/(34*22 + 67)
# A = (8400 - 22B) / 94
# B = (finaly_y - Ay*final_x) / (Ay * Ax + Ay)
# A = (final_x - Bx * B) / Ax

# A*ax + B*bx = final_x
# A*ay + B*by = final_y

# A = (final_x - B*bx) / ax
# ((final_x - B*bx) / ax)*ay + B*by = final_y
# (ay * final_x - B * ay * bx)/ay + B* by = final_y
# (final_x - B )
from dataclasses import dataclass


final_y = 5400
final_x = 8400
Ax = 94
Ay = 34
Bx = 22
By = 67

A = (final_y - (By * final_x / Bx)) / (Ay - By * Ax / Bx)
B = (final_x - Ax * A) / Bx

# Button A: X+17, Y+86
# Button B: X+84, Y+37
# Prize: X=7870, Y=6450

final_x = 7870
final_y = 6450
Ax = 17
Ay = 86
Bx = 84
By = 37


# Button A: X+26, Y+66
# Button B: X+67, Y+21
# Prize: X=12748, Y=12176
final_x = 12748
final_y = 12176
Ax = 26
Ay = 66
Bx = 67
By = 21


@dataclass
class Equation:
    final_x: int
    final_y: int
    Ax: int
    Ay: int
    Bx: int
    By: int

    def solve(self):
        A = (self.final_x * self.By - self.final_y * self.Bx) / (self.Ax * self.By - self.Ay * self.Bx)
        B = (self.final_y * self.Ax - self.final_x * self.Ay) / (self.Ax * self.By - self.Ay * self.Bx)
        return (A, B)


with open("input.txt", "r") as f:
    lines = f.read().splitlines()

final_x: int = -1
final_y: int = -1
Ax: int = -1
Ay: int = -1
Bx: int = -1
By: int = -1
equations: list[Equation] = []
for i, line in enumerate(lines):
    if i % 4 == 0:
        # Button A
        Ax = re.search(r"X\+(\d+)", line).groups()[0]
        Ay = re.search(r"Y\+(\d+)", line).groups()[0]
    elif i % 4 == 1:
        # Button B
        Bx = re.search(r"X\+(\d+)", line).groups()[0]
        By = re.search(r"Y\+(\d+)", line).groups()[0]
    elif i % 4 == 2:
        # Prize
        final_x = re.search(r"X=(\d+)", line).groups()[0]
        final_y = re.search(r"Y=(\d+)", line).groups()[0]
    elif i % 4 == 3:
        assert line == ""
        equations.append(
            Equation(int(final_x), int(final_y), int(Ax), int(Ay), int(Bx), int(By))
        )

price = 0
for equation in equations:
    a, b = equation.solve()
    print(i, a, a % 1 == 0, b, b % 1 == 0)
    if not a.is_integer() or not b.is_integer():
        continue
    price += a * 3
    price += b
print(price)
