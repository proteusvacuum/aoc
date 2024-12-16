from dataclasses import dataclass
from typing import Iterable


with open("input.txt", "r") as f:
    lines = f.read().splitlines()

max_x = len(lines)
max_y = len(lines[0])

# Collect contigous regions
# Area = number of items in the region
# Perimiter = Length of sides

# A side to count - is touching a different item
# Count number of sides that are touching different squares

@dataclass
class Plant:
    name: str
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



@dataclass
class Garden:
    plants: list[Plant]
    plants_by_coord: dict[tuple, Plant]

    def get_cost(self):
        total_cost = 0
        regions = self.get_regions()
        for region in regions:
            region_area = len(region)
            region_fence_cost = 0
            for plant in region:
                region_fence_cost += self.fenced_edges_for_plant(plant)
            total_cost += region_area * region_fence_cost
        return total_cost

    def get_regions(self):
        regions: list[list[Plant]] = []
        seen_plants = set()
        for plant in self.plants:
            if plant in seen_plants:
                continue
            region = self.get_plant_region(plant)
            regions.append(region)
            seen_plants |= set([p for p in region])
        return regions

    def get_plant_region(self, plant: Plant) -> list[Plant]:
        connected_plants: list[Plant] = [plant]
        plants_to_check = [plant]
        seen_plants = set([plant])
        while len(plants_to_check):
            checking_plant = plants_to_check.pop()
            for edge_to_check in checking_plant.edges:
                new_plant = plants_by_position[edge_to_check]
                if new_plant in seen_plants:
                    continue
                if new_plant.name == checking_plant.name:
                    connected_plants.append(new_plant)
                    plants_to_check.append(new_plant)
                seen_plants.add(new_plant)
        return connected_plants

    def get_all_fenced_edges(self):
        count = 0
        for plant in plants:
            count += self.fenced_edges_for_plant(plant)
        return count

    def fenced_edges_for_plant(self, plant: Plant):
        count = 0
        try:
            if self.plants_by_coord[(plant.position[0] + 1, plant.position[1])].name != plant.name:
                count += 1
        except KeyError:
            count += 1
        try:
            if self.plants_by_coord[(plant.position[0] - 1, plant.position[1])].name != plant.name:
                count += 1
        except KeyError:
            count += 1
        try:
            if self.plants_by_coord[(plant.position[0], plant.position[1] + 1)].name != plant.name:
                count += 1
        except KeyError:
            count += 1
        try:
            if self.plants_by_coord[(plant.position[0], plant.position[1] - 1)].name != plant.name:
                count += 1
        except KeyError:
            count += 1
        return count


plants_by_position = {}
plants = []
seen_plant_names = set()

for column, line in enumerate(lines):
    for row, plant_name in enumerate(line):
        position = (row, column)
        plant = Plant(plant_name, position)
        plants_by_position[position] = plant
        plants.append(plant)
garden = Garden(plants, plants_by_position)
print(garden.get_cost())
