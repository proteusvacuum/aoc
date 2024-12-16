from dataclasses import dataclass
from typing import Iterable


with open("input.txt", "r") as f:
    lines = f.read().splitlines()

max_x = len(lines)
max_y = len(lines[0])


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

    def get_num_corners_plant(self, plant: Plant):
        class FakePlant:
            def __init__(self):
                self.name = ""

        num_corners = 0
        left = self.plants_by_coord.get(
            (plant.position[0] - 1, plant.position[1]), FakePlant()
        )
        right = self.plants_by_coord.get(
            (plant.position[0] + 1, plant.position[1]), FakePlant()
        )
        up = self.plants_by_coord.get(
            (plant.position[0], plant.position[1] - 1), FakePlant()
        )
        down = self.plants_by_coord.get(
            (plant.position[0], plant.position[1] + 1), FakePlant()
        )
        top_left = self.plants_by_coord.get(
            (plant.position[0] - 1, plant.position[1] - 1), FakePlant()
        )
        top_right = self.plants_by_coord.get(
            (plant.position[0] + 1, plant.position[1] - 1), FakePlant()
        )
        bottom_left = self.plants_by_coord.get(
            (plant.position[0] - 1, plant.position[1] + 1), FakePlant()
        )
        bottom_right = self.plants_by_coord.get(
            (plant.position[0] + 1, plant.position[1] + 1), FakePlant()
        )

        # Outer corner
        if up.name != plant.name and left.name != plant.name:
            num_corners += 1
        # Inner corner
        if up.name == left.name == plant.name and top_left.name != plant.name:
            num_corners += 1

        if up.name != plant.name and right.name != plant.name:
            num_corners += 1
        if up.name == right.name == plant.name and top_right.name != plant.name:
            num_corners += 1

        if down.name != plant.name and right.name != plant.name:
            num_corners += 1
        if down.name == right.name == plant.name and bottom_right.name != plant.name:
            num_corners += 1

        if down.name != plant.name and left.name != plant.name:
            num_corners += 1
        if down.name == left.name == plant.name and bottom_left.name != plant.name:
            num_corners += 1

        return num_corners

    def get_num_corners(self, region: list[Plant]):
        corners = 0
        # single item in the region = 4 corners
        if len(region) == 1:
            return 4
        for plant in region:
            corners += self.get_num_corners_plant(plant)
        return corners

    def get_cost(self):
        total_cost = 0
        regions = self.get_regions()
        for region in regions:
            region_area = len(region)
            region_fence_cost = self.get_num_corners(region)
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
