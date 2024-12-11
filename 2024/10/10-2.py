from dataclasses import dataclass
from collections import defaultdict
from typing import Iterable

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

max_x = len(lines)
max_y = len(lines[0])


@dataclass
class Node:
    height: int
    position: tuple

    def __hash__(self):
        return hash(self.position)

    @property
    def edges(self) -> Iterable[tuple]:
        if self.position[0] + 1 < max_x:
            yield (self.position[0] + 1, self.position[1])
        if self.position[0] - 1 >= 0:
            yield (self.position[0] - 1, self.position[1])
        if self.position[1] + 1 < max_y:
            yield (self.position[0], self.position[1] + 1)
        if self.position[1] - 1 >= 0:
            yield (self.position[0], self.position[1] - 1)


start_nodes: list[Node] = []
nodes_by_position: dict[tuple, Node] = {}


for column, line in enumerate(lines):
    for row, node_name in enumerate(line):
        if node_name == ".":
            continue
        position = (row, column)
        node = Node(int(node_name), position)
        nodes_by_position[position] = node
        if int(node_name) == 0:
            start_nodes.append(node)


def get_connected_nodes(node: Node) -> list[Node]:
    connected_nodes: list[Node] = []
    for edge_to_check in node.edges:
        try:
            if nodes_by_position[edge_to_check].height == node.height + 1:
                connected_nodes.append(nodes_by_position[edge_to_check])
        except KeyError:
            continue
    return connected_nodes


def dfs(node: Node):
    score = 0
    nodes: list[Node] = get_connected_nodes(node)
    while len(nodes):
        node_to_check = nodes.pop()
        if node_to_check.height == 9:
            score += 1
        nodes.extend(get_connected_nodes(node_to_check))
    return score


output = 0
for start_node in start_nodes:
    output += dfs(start_node)
print(output)
