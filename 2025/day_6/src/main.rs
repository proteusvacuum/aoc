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

fn parse_input_2(input: &str) -> (Vec<Vec<usize>>, Vec<String>) {
    // Read each column.
    let lines: Vec<&str> = input.lines().collect();
    let reversed_lines: Vec<String> = lines
        .iter()
        .map(|l| l.chars().rev().collect::<String>())
        .collect();

    // collect characters until I get an operator, then skip a character and start again.

    let mut values: Vec<Vec<usize>> = vec![];
    let mut operators: Vec<String> = vec![];

    let number_length = reversed_lines.len();
    let num_columns = reversed_lines[0].len();
    let mut row_index = 0 as usize;
    let mut column_index: usize = 0;
    let mut nums: Vec<usize> = vec![];

    loop {
        if column_index >= num_columns {
            break;
        }
        dbg!(column_index);
        // the columns
        let mut value = String::new();
        loop {
            if row_index >= number_length {
                nums.push(value.parse().unwrap());
                row_index = 0;
                column_index += 1;
                break;
            }
            if let Some(ch) = reversed_lines[row_index].chars().nth(column_index) {
                match ch {
                    '+' | '*' => {
                        operators.push(ch.to_string());
                        nums.push(value.parse().unwrap());
                        values.push(nums.clone());
                        nums = vec![];
                        row_index = 0;
                        column_index += 2;
                        break;
                    }
                    ' ' => {
                        row_index += 1;
                    }
                    _ => {
                        value.push(ch);
                        row_index += 1;
                    }
                }
            } else {
                panic!()
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
        .map(|(i, v)| match operators[i].as_str() {
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
