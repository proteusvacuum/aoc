with open("input.txt", "r") as f:
    line = f.read()

nums = [int(n) for n in line.split(" ")]

new_nums = []

for _ in range(25):
    for num in nums:
        if num == 0:
            new_nums.append(1)
        elif len(str(num)) % 2 == 0:
            str_num = str(num)
            new_nums.append(int(str_num[0 : len(str_num) // 2]))
            new_nums.append(int(str_num[len(str_num) // 2:]))
        else:
            new_nums.append(num * 2024)
    nums = new_nums
    new_nums = []
print(len(nums))
