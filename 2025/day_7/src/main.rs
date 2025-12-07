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

    fn set(&mut self, coord: Coord, value: char) {
        let cell_id = self.cell_id(coord);
        self.cells[cell_id] = value;
    }

    fn set_left(&mut self, coord: Coord, value: char) {
        let nx = coord.x as isize - 1;
        let ny = coord.y;
        if nx < 0 {
            return;
        }
        let new_coord = Coord {
            x: nx as usize,
            y: ny,
        };
        let cell_id = self.cell_id(new_coord);
        self.cells[cell_id] = value;
    }

    fn set_right(&mut self, coord: Coord, value: char) {
        let nx = coord.x + 1;
        let ny = coord.y;
        if nx > self.width {
            return;
        }
        let new_coord = Coord { x: nx, y: ny };
        let cell_id = self.cell_id(new_coord);
        self.cells[cell_id] = value;
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

    fn above(&self, coord: &Coord) -> Option<(Coord, char)> {
        // What is above this cell?
        let nx = coord.x;
        let ny = coord.y as isize - 1;
        if ny < 0 {
            return None;
        }

        let new_coord: Coord = Coord {
            x: nx,
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
    Grid::new(input.lines().count(), width, cells)
}

fn solve_part1(input: &str) -> usize {
    // For each row
    // For item.
    // If item == ., if the item above is a beam, the item becomes a beam.
    // If item == ^, if the item above is a beam, the items before and after become a beam

    // Notes: There are no splitters directly next to each other.

    let mut count = 0;
    let grid = parse_input(input);
    let mut new_grid = grid.clone();

    grid.iter_values().for_each(|(coord, c)| {
        let current_char = c.unwrap();
        if let Some((_, above)) = new_grid.above(&coord) {
            match current_char {
                '.' => match above {
                    'S' | '|' => {
                        new_grid.set(coord, '|');
                    }
                    _ => {}
                },
                '^' => match above {
                    'S' | '|' => {
                        // On either side we set it as a '|'
                        new_grid.set_left(coord, '|');
                        new_grid.set_right(coord, '|');
                        count += 1;
                    }
                    _ => {}
                },
                _ => {}
            };
        }
    });

    count
}

fn solve_part2_again(input: &str) -> usize {
    // Every time a splitter is hit, we create 2N particles.
    // NOTE: I chatted with Claude about this approach, but coded this up myself.
    // Store the number of particles flowing down each branch, then count it at the end

    // let mut count = 1;
    // let grid = parse_input(input);
    // let mut new_grid = grid.clone();

    // grid.iter_values().for_each(|(coord, c)| {
    //     let current_char = c.unwrap();
    //     if let Some((_, above)) = new_grid.above(&coord) {
    //         match current_char {
    //             '.' => match above {
    //                 'S' | '|' => {
    //                     new_grid.set(coord, '|');
    //                 }
    //                 _ => {}
    //             },
    //             '^' => match above {
    //                 'S' | '|' => {
    //                     // On either side we set it as a '|'
    //                     new_grid.set_left(coord, '|');
    //                     new_grid.set_right(coord, '|');
    //                     count *= 2;
    //                 }
    //                 _ => {}
    //             },
    //             _ => {}
    //         };
    //     }
    // });

    // count
    todo!();
}

fn solve_part2(input: &str) -> usize {
    // NOTE: Too slow!
    // At every splitter, we create a new world, where the beam goes in every possible direction.

    let grid = parse_input(input);

    fn split_world(grid: &Grid, starting_idx: usize, mut count: usize) -> usize {
        let mut new_grid = grid.clone();
        grid.iter_values()
            .enumerate()
            .skip(starting_idx)
            .for_each(|(idx, (coord, c))| {
                let current_char = c.unwrap();
                if let Some((_, above)) = new_grid.above(&coord) {
                    match current_char {
                        '.' => match above {
                            'S' | '|' => {
                                new_grid.set(coord, '|');
                            }
                            _ => {}
                        },
                        '^' => match above {
                            'S' | '|' => {
                                // In our timeline model, we set left and spawn a world,
                                let mut left_world = new_grid.clone();
                                left_world.set_left(coord, '|');

                                let mut right_world = new_grid.clone();
                                right_world.set_right(coord, '|');
                                count = split_world(&left_world, idx + 1, count)
                                    + split_world(&right_world, idx + 1, count);
                            }
                            _ => {}
                        },
                        _ => {}
                    };
                }
            });
        println!("{}", new_grid);
        println!("---");
        count
    }

    split_world(&grid, 0, 1)
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
        assert_eq!(solve_part1(SAMPLE1), 21);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(SAMPLE1), 40);
        assert_eq!(solve_part2_again(SAMPLE1), 40);
    }
}
