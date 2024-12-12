from collections import defaultdict


with open("input.txt", "r") as f:
    line = f.read()

stones = [int(n) for n in line.split(" ")]

stone_counts = defaultdict(int)
for stone in stones:
    stone_counts[stone] += 1
print(stone_counts)

for _ in range(75):
    print(_)
    new_stone_counts = stone_counts.copy()

    for stone_value, stone_count in stone_counts.items():
        for i in range(stone_count):
            if stone_value == 0:
                new_stone_counts[0] -= 1
                new_stone_counts[1] += 1
            elif len(str(stone_value)) % 2 == 0:
                new_stone_counts[stone_value] -= 1
                str_num = str(stone_value)
                first_half = int(str_num[:len(str_num) // 2])
                second_half = int(str_num[len(str_num) // 2:])
                new_stone_counts[first_half] += 1
                new_stone_counts[second_half] += 1
            else:
                new_stone_counts[stone_value] -= 1
                new_stone_counts[stone_value * 2024] += 1

    stone_counts = new_stone_counts.copy()

print(sum(stone_counts.values()))
