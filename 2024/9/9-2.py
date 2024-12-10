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


def find_subsequence(haystack, needle):
    return [i for i in range(len(haystack)) if haystack[i : i + len(needle)] == needle]


seen_files = set()
num_spaces = len([f for f in new_files if f == "."])
for i in range(len(new_files), 0, -1):
    if new_files[i - 1] == ".":
        continue
    if new_files[i - 1] in seen_files:
        continue
    seen_files.add(new_files[i - 1])
    print("moving: ", new_files[i - 1])
    num_files = new_files.count(new_files[i - 1])
    empty_spots = find_subsequence(new_files, ["."] * num_files)
    if empty_spots:
        first_pos = empty_spots[0]
    else:
        continue
    if first_pos >= i:
        continue
    new_files[first_pos : first_pos + num_files] = new_files[i - num_files : i]
    new_files[i - num_files : i] = ["."] * num_files


checksum = 0
for i, item in enumerate(new_files):
    if item != ".":
        checksum += i * item

print(checksum)
