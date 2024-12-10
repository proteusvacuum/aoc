with open("input.txt", "r") as f:
    line = f.read().splitlines()[0]

files = line[::2]
spaces = line[1::2]


checksum = 0
new_files = []
num_spaces = 0
for i in range(len(files)):
    new_files.extend([i] * int(files[i]))
    if i < len(spaces):
        new_files.extend(["."] * int(spaces[i]))
        num_spaces += int(spaces[i])


num_spaces = len([f for f in new_files if f == "."])
for i in range(len(new_files), 0, -1):
    if new_files[i - 1] == ".":
        continue
    first_pos = new_files.index(".")
    new_files[first_pos] = new_files[i - 1]
    new_files[i - 1] = "."
    if all(
        f == "."
        for f in new_files[len(new_files) - 1 : len(new_files) - 1 - num_spaces : -1]
    ):
        break


checksum = 0
for i, item in enumerate(new_files):
    if item != ".":
        checksum += i * item

print(checksum)
