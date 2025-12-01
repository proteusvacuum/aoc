#[derive(Debug, Eq, PartialEq)]
enum Direction {
    Left,
    Right,
}

impl From<char> for Direction {
    fn from(value: char) -> Self {
        match value {
            'L' => Direction::Left,
            'R' => Direction::Right,
            _ => panic!(),
        }
    }
}

#[derive(Debug)]
struct Movement {
    direction: Direction,
    clicks: i32,
}
impl From<&str> for Movement {
    fn from(value: &str) -> Self {
        Movement {
            direction: value.chars().nth(0).unwrap().into(),
            clicks: value[1..].parse().unwrap(),
        }
    }
}

fn parse_input(input: &str) -> Vec<Movement> {
    input.lines().map(|l| l.into()).collect()
}

fn solve_part1(input: &str) -> i32 {
    // Count the number of zeros
    let movements = parse_input(input);
    let mut position: i32 = 50;
    let mut count = 0;

    for movement in movements {
        match movement.direction {
            Direction::Left => position = (position - movement.clicks).rem_euclid(100),
            Direction::Right => position = (position + movement.clicks).rem_euclid(100),
        }
        if position == 0 {
            count += 1
        }
    }
    count
}

fn solve_part2(input: &str) -> i32 {
    // Count how many times we roll over
    let movements = parse_input(input);
    let mut position: i32 = 50;
    let mut count = 0;

    for movement in movements {
        let new_position = match movement.direction {
            Direction::Left => position - movement.clicks,
            Direction::Right => position + movement.clicks,
        };
        let crossings = new_position.div_euclid(100).abs();
        count += crossings;
        position = new_position.rem_euclid(100);
    }
    count
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
        assert_eq!(solve_part1(SAMPLE1), 3);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(SAMPLE1), 6);
        assert_eq!(solve_part2("R1000"), 10);
    }
}
