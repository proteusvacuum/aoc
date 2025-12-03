fn parse_input(input: &str) -> Vec<Vec<u32>> {
    input
        .lines()
        .map(|l| l.chars().map(|c| c.to_digit(10).unwrap()).collect())
        .collect()
}

fn solve_part1(input: &str) -> usize {
    let mut sum = 0;
    let banks = parse_input(input);
    for bank in banks {
        // Find the largest number, and its index in the bank (except the last number)
        let mut sorted_bank = bank[..bank.len() - 1]
            .iter()
            .enumerate()
            .collect::<Vec<(usize, &u32)>>();
        sorted_bank.sort_by_key(|&(_i, v)| std::cmp::Reverse(v));
        let largest = sorted_bank[0];
        // Get the maximum of the remaining items
        let second = bank[largest.0 + 1..].iter().max().unwrap();
        let max_jolts = format!("{}{}", largest.1.to_string(), second.to_string())
            .parse::<usize>()
            .unwrap();
        sum += max_jolts;
    }
    sum
}

fn solve_part2(input: &str) -> usize {
    const BANK_SIZE: usize = 12;
    let mut sum: usize = 0;
    let banks = parse_input(input);
    for bank in banks {
        // Sliding window. Find the largest value inside of the next set.
        // The window size starts from previous_index + 1. We need num_items_we_need after the window.
        let mut prev_largest_index: usize = 0;
        let mut digits: [u32; BANK_SIZE] = [0; BANK_SIZE];
        let mut digits_needed = BANK_SIZE;
        for digit in 0..BANK_SIZE {
            let last_index = bank.len() - digits_needed;
            let mut sorted_bank = bank[prev_largest_index..=last_index]
                .iter()
                .enumerate()
                .collect::<Vec<(usize, &u32)>>();
            sorted_bank.sort_by_key(|&(_i, v)| std::cmp::Reverse(v));
            digits[digit] = *sorted_bank[0].1;
            prev_largest_index = sorted_bank[0].0 + prev_largest_index + 1;
            digits_needed -= 1;
        }
        let max_jolts = digits
            .iter()
            .map(|d| d.to_string())
            .collect::<Vec<String>>()
            .join("")
            .parse::<usize>()
            .unwrap();
        sum += max_jolts;
    }
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

    #[ignore]
    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(SAMPLE1), 357);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(SAMPLE1), 3121910778619);
    }
}
