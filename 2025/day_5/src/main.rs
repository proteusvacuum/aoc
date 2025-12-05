use std::ops::Range;

fn parse_input(input: &str) -> (Vec<Range<usize>>, Vec<usize>) {
    let mut database: Vec<Range<usize>> = vec![];
    let mut values: Vec<usize> = vec![];
    input.lines().for_each(|l| {
        if l.contains("-") {
            let (first_s, last_s) = l.split_once("-").unwrap();
            let start = first_s.parse::<usize>().unwrap();
            let end = last_s.parse::<usize>().unwrap();
            let range = Range {
                start,
                end: end + 1, // Ranges are exclusive
            };
            database.push(range);
        } else if l != "" {
            values.push(l.parse::<usize>().unwrap());
        }
    });

    (database, values)
}

fn solve_part1(input: &str) -> usize {
    let (database, values) = parse_input(input);
    values
        .iter()
        .filter(|v| database.iter().any(|r| r.contains(v)))
        .count()
}

fn solve_part2(input: &str) -> usize {
    let (mut database, _) = parse_input(input);

    // Merge the overlapping ranges
    // There aren't that many ranges, so it isn't that bad.
    // [1..5]
    // [3..4] (remove this one) : completely subsumed
    // [2..6] becomes -> [1..6] (ends after)
    // [-1..3] becomes -> [-1..0] (begins before)
    // Then we just do end-start on each range and get the sum.
    // Sort the ranges, then check if we are inside.

    database.sort_by_key(|r| r.start);
    let mut new_ranges: Vec<Range<usize>> = vec![database[0].clone()];

    for range in database.into_iter().skip(1) {
        let last = new_ranges.last_mut().unwrap();
        if range.start <= last.end {
            // If this is overlapping with the last one, grow it as necessary
            last.end = last.end.max(range.end)
        } else {
            new_ranges.push(range.clone());
        }
    }

    new_ranges.iter().map(|r| r.end - r.start).sum()
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
        assert_eq!(solve_part2(SAMPLE1), 14);
    }
}
