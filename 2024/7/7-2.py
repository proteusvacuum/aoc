from dataclasses import dataclass
from itertools import product


with open("input.txt", "r") as f:
    lines = f.read().splitlines()


def concat(left: int, right: int):
    return int(f"{left}{right}")


@dataclass
class Equation:
    result: int
    values: list[int]

    def is_equal(self, operators):
        output = self.values[0]
        for idx, operator in enumerate(operators):
            if operator == "+":
                output += self.values[idx + 1]
            elif operator == "*":
                output *= self.values[idx + 1]
            elif operator == "|":
                output = concat(output, self.values[idx + 1])
        return output == self.result


equations: list[Equation] = []

for line in lines:
    result, values = line.split(": ")
    values = [int(v) for v in values.split(" ")]
    equations.append(Equation(int(result), values))

output = 0
for equation in equations:
    num_operators = len(equation.values) - 1
    permutations = list(product(*["+*|" for _ in range(num_operators)]))
    for permutation in permutations:
        if equation.is_equal(permutation):
            output += equation.result
            break

print(output)
