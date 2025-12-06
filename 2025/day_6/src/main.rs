fn parse_input_1(input: &str) -> (Vec<Vec<usize>>, Vec<&str>) {
    // There can be more than one whitspace char
    // Read through each line and create nested lists
    let num_items = input
        .lines()
        .next()
        .unwrap()
        .split_ascii_whitespace()
        .clone()
        .count();
    let mut values: Vec<Vec<usize>> = vec![vec![]; num_items];
    let mut operators: Vec<&str> = vec![];
    for line in input.lines() {
        for (idx, value) in line.split_ascii_whitespace().enumerate() {
            match value {
                "*" | "+" => operators.push(value),
                _ => values[idx].push(value.parse::<usize>().unwrap()),
            }
        }
    }
    (values, operators)
}

fn parse_input_2(input: &str) -> (Vec<Vec<usize>>, Vec<&str>) {
    // Read characters right to left.
    // We know the split boundary based on the index of the operator.

    let mut lines: Vec<String> = input.lines().map(|l| l.chars().rev().collect()).collect();
    let operators = lines[lines.len() - 1].clone();
    lines = lines[0..lines.len() - 1].to_vec();

    let number_boundaries: Vec<usize> = operators
        .char_indices()
        .filter(|(_, ch)| !ch.is_whitespace())
        .map(|(idx, _)| idx)
        .collect();

    // Read number_boundaries chars from each line
    // Read top to bottom, as we did in part one
    dbg!(&lines, &operators, &number_boundaries);

    dbg!(lines
        .iter()
        .enumerate()
        .map(|(line_num, line)| {
            number_boundaries
                .iter()
                .enumerate()
                .map(|(n, nb)| {
                    line.chars()
                        .skip(number_boundaries[n - 1])
                        .take(*nb)
                        .collect::<String>()
                })
                .collect()
        })
        .collect::<Vec<String>>());

    for (line_num, line) in lines.iter().enumerate() {
        dbg!(line
            .chars()
            .take(number_boundaries[0] + 1)
            .collect::<String>());
    }

    let num_items = input
        .lines()
        .next()
        .unwrap()
        .split_ascii_whitespace()
        .clone()
        .count();
    let mut values: Vec<Vec<usize>> = vec![vec![]; num_items];
    let mut operators: Vec<&str> = vec![];
    for line in input.lines() {
        for (idx, value) in line.split_ascii_whitespace().enumerate() {
            match value {
                "*" | "+" => operators.push(value),
                _ => values[idx].push(value.parse::<usize>().unwrap()),
            }
        }
    }
    (values, operators)
}

fn solve_part1(input: &str) -> usize {
    let (values, operators) = parse_input_1(input);
    values
        .iter()
        .enumerate()
        .map(|(i, v)| match operators[i] {
            "*" => v.iter().fold(1 as usize, |num, accum| accum * num),
            "+" => v.iter().sum(),
            _ => panic!(),
        })
        .sum()
}

fn solve_part2(input: &str) -> usize {
    let (values, operators) = parse_input_2(input);
    dbg!(&values, &operators);
    values
        .iter()
        .enumerate()
        .map(|(i, v)| match operators[i] {
            "*" => v.iter().fold(1 as usize, |num, accum| accum * num),
            "+" => v.iter().sum(),
            _ => panic!(),
        })
        .sum()
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
        assert_eq!(solve_part1(SAMPLE1), 4277556);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(SAMPLE1), 3263827);
    }
}
