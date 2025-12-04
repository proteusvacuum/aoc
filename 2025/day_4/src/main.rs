use std::fmt::Display;

#[derive(Debug, Clone, Copy)]
struct Coord {
    x: usize,
    y: usize,
}

#[derive(Debug, Clone)]
struct Grid {
    height: usize,    // y
    width: usize,     // x
    cells: Vec<char>, // Use a flat vec, we can calculate the indices based on the height / width
}
impl Grid {
    fn new(height: usize, width: usize, cells: Vec<char>) -> Self {
        Self {
            height,
            width,
            cells,
        }
    }

    fn cell_id(&self, coord: Coord) -> usize {
        coord.y * self.width + coord.x
    }

    fn get(&self, coord: Coord) -> Option<char> {
        self.cells.get(self.cell_id(coord)).copied()
    }

    fn in_bounds(&self, coord: Coord) -> bool {
        coord.x < self.width && coord.y < self.height
    }

    fn iter_values(&self) -> impl Iterator<Item = (Coord, Option<char>)> {
        self.cells.iter().enumerate().map(|(i, v)| {
            let x = i % self.width;
            let y = i / self.width;
            (Coord { x, y }, Some(*v))
        })
    }

    fn count_movable_rolls(&self) -> usize {
        self.iter_values()
            .filter(|(c, v)| {
                // If this is a paper roll, and there are less than 4 neighbouring paper rolls
                v == &Some('@') && self.neighbours(c).filter(|(_, n)| n == &'@').count() < 4
            })
            .count()
    }

    fn neighbours(&self, coord: &Coord) -> impl Iterator<Item = (Coord, char)> {
        const DIRECTIONS: [(isize, isize); 8] = [
            (-1, -1),
            (0, -1),
            (1, -1),
            (-1, 0),
            (1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
        ];

        DIRECTIONS.into_iter().filter_map(move |(dx, dy)| {
            let nx = coord.x as isize + dx;
            let ny = coord.y as isize + dy;

            if nx < 0 || ny < 0 {
                return None;
            }

            let new_coord: Coord = Coord {
                x: nx as usize,
                y: ny as usize,
            };

            if self.in_bounds(new_coord) {
                Some((
                    new_coord,
                    self.get(new_coord).expect("out of bounds somehow"),
                ))
            } else {
                None
            }
        })
    }
}

impl Display for Grid {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for y in 0..self.height {
            for x in 0..self.width {
                let idx = y * self.width + x;
                write!(f, "{}", self.cells[idx])?;
            }
            if y + 1 < self.height {
                writeln!(f)?;
            }
        }
        Ok(())
    }
}

fn parse_input(input: &str) -> Grid {
    let width = input.lines().next().unwrap().len();
    let cells: Vec<char> = input.lines().flat_map(str::chars).collect();
    Grid::new(width, input.lines().count(), cells)
}

fn solve_part1(input: &str) -> usize {
    let grid = parse_input(input);
    // Iterate over the grid, count number of neighbouring rolls
    grid.count_movable_rolls()
}

fn step(grid: &Grid) -> (Grid, usize) {
    let mut new_grid = grid.clone();

    let mut changed = 0;

    for (coord, val) in grid.iter_values() {
        if val == Some('@') && grid.neighbours(&coord).filter(|(_, n)| n == &'@').count() < 4 {
            let id = new_grid.cell_id(coord);
            new_grid.cells[id] = 'x';
            changed += 1;
        }
    }

    (new_grid, changed)
}

fn solve_part2(input: &str) -> usize {
    let mut grid = parse_input(input);
    let mut sum = 0;
    loop {
        let changed;
        (grid, changed) = step(&grid);
        sum += changed;
        if changed == 0 {
            break;
        }
    }
    // This is like game of life - kill neighbours, until there are none left to kill.
    sum
}

fn main() {
    let input = include_str!("../input.txt");
    println!("Part 1: {}", solve_part1(input));
    println!("Part 2: {}", solve_part2(input));
}

#[cfg(test)]
mod tests {
    use super::*;
    static SAMPLE1: &str = include_str!("../test_1.txt");

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(SAMPLE1), 13);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(SAMPLE1), 43);
    }
}
