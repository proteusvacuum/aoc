from collections import defaultdict
from functools import cmp_to_key, partial


with open('input.txt', 'r') as f:
    lines = f.read().splitlines()


before = defaultdict(list)
after = defaultdict(list)
updates = []


def parse_rules(line):
    rule = line.split("|")
    before[int(rule[0])].append(int(rule[1]))
    after[int(rule[1])].append(int(rule[0]))

def parse_updates(line):
     updates.append([int(l) for l in line.split(",")])


parsing_rules = True
for line in lines:
    if line == "":
        parsing_rules = False
        continue
    if parsing_rules:
        parse_rules(line)
    else:
        parse_updates(line)

def check_update(update: list):
    for item in update:
        for before_item in before[item]:
            if before_item in update and update.index(before_item) < update.index(item):
                return False
        for after_item in after[item]:
            if after_item in update and update.index(after_item) > update.index(item):
                return False
    return True


def get_middle_item(update:list):
    return update[len(update) // 2]


def reorder_update(update: list):
    def sort_fn(item1, item2):
        if item2 in before[item1]:
            return -1
        return 1

    return sorted(update, key=cmp_to_key(sort_fn))

output = 0
for update in updates:
    if not check_update(update):
        output += get_middle_item(reorder_update(update))

print(output)
