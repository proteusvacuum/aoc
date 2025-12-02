// Loop through each number in the range.
// Cut the number in half, if the two halves are the same, add it.

use std::str::FromStr;

#[derive(Debug)]
struct Range {
    start: usize,
    end: usize,
}
impl FromStr for Range {
    type Err = &'static str;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        let (start, end) = value.split_once("-").ok_or("yikes")?;
        Ok(Self {
            start: start.parse().unwrap(),
            end: end.parse().unwrap(),
        })
    }
}

fn parse_input(input: &str) -> Vec<Range> {
    input
        .lines()
        .next()
        .expect("empty")
        .split(",")
        .map(|r| r.parse().unwrap())
        .collect()
}

fn solve_part1(input: &str) -> usize {
    let ranges = parse_input(input);
    let mut invalid_id_sum = 0;
    for r in &ranges {
        for n in r.start..=r.end {
            let s = n.to_string();
            let (left, right) = s.split_at(s.len() / 2);
            if left == right {
                invalid_id_sum += n
            }
        }
    }
    invalid_id_sum
}

fn is_invalid_id(id: &str) -> bool {
    let bytes = id.as_bytes();
    let length = id.len();
    let longest_subsequence = length / 2;

    for subsequence_length in 1..=longest_subsequence {
        // split the string into chunks, test they are all the same;
        let mut iter = bytes.chunks(subsequence_length);
        let first = iter.next().unwrap();
        if iter.all(|i| i == first) {
            return true;
        }
    }

    false
}

fn solve_part2(input: &str) -> usize {
    let ranges = parse_input(input);
    let mut invalid_id_sum = 0;
    for r in &ranges {
        for n in r.start..=r.end {
            let s = n.to_string();
            if is_invalid_id(&s) {
                invalid_id_sum += n
            }
        }
    }
    invalid_id_sum
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
        assert_eq!(solve_part1(SAMPLE1), 1227775554);
    }

    #[test]
    fn test_part2() {
        assert!(is_invalid_id("11"));
        assert!(is_invalid_id("111"));
        assert!(is_invalid_id("11221122"));
        assert_eq!(solve_part2(SAMPLE1), 4174379265);
    }
}
