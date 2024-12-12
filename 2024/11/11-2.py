from collections import defaultdict


with open("input.txt", "r") as f:
    line = f.read()

stones = [int(n) for n in line.split(" ")]

stone_counts = defaultdict(int)
for stone in stones:
    stone_counts[stone] += 1

for _ in range(75):
    new_stone_counts = stone_counts.copy()
    for stone_value, stone_count in stone_counts.items():
        if stone_count == 0:
            del new_stone_counts[stone_value]
            continue
        if stone_value == 0:
            new_stone_counts[0] -= stone_count
            new_stone_counts[1] += stone_count
        elif len(str(stone_value)) % 2 == 0:
            new_stone_counts[stone_value] -= stone_count
            str_num = str(stone_value)
            first_half = int(str_num[: len(str_num) // 2])
            second_half = int(str_num[len(str_num) // 2 :])
            new_stone_counts[first_half] += stone_count
            new_stone_counts[second_half] += stone_count
        else:
            new_stone_counts[stone_value] -= stone_count
            new_stone_counts[stone_value * 2024] += stone_count

    stone_counts = new_stone_counts
print(sum(stone_counts.values()))
