#include <cmath>
#include <cstddef>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

std::vector<std::string> split(const std::string &input,
                               std::string delimiter) {
  std::vector<std::string> tokens;
  size_t start = 0;
  size_t end = input.find(delimiter);

  while (end != std::string::npos) {
    tokens.push_back(input.substr(start, end - start));
    start = end + delimiter.size();
    end = input.find(delimiter, start);
  }

  tokens.push_back(input.substr(start));
  return tokens;
};

bool isNextUnsafe(int first_item, int second_item, bool prev_decreasing) {
  bool decreasing = (first_item - second_item) < 0;
  return (std::abs(second_item - first_item) > 3 || second_item == first_item ||
          prev_decreasing != decreasing);
}

bool isListSafe(std::vector<std::string> &items) {
  bool prev_decreasing = (std::stoi(items[0]) - std::stoi(items[1])) < 0;
  for (int i = 0; i < items.size() - 1; ++i) {
    int first_item = std::stoi(items[i]);
    int second_item = std::stoi(items[i + 1]);
    std::cout << second_item << "-" << first_item << " = "
              << std::abs(second_item - first_item);
    if (isNextUnsafe(first_item, second_item, prev_decreasing)) {
      std::cout << " unsafe!";
      return false;
    }
    std::cout << std::endl;
    prev_decreasing = (first_item - second_item) < 0;
  }
  return true;
};

int main() {
  std::string line;
  int safe_count = 0;
  while (std::getline(std::cin, line)) {
    std::cout << "----" << std::endl;
    std::vector<std::string> items = split(line, " ");
    if (isListSafe(items)) {
      ++safe_count;
    } else {
      std::cout << "---" << std::endl;
      for (int i = 0; i < items.size(); ++i) {
        // remove each item in turn and try again
        std::vector<std::string> new_items;
        for (int j = 0; j < items.size(); ++j) {
          if (i != j) {
            new_items.emplace_back(items[j]);
          }
        }
        if (isListSafe(new_items)) {
          std::cout << "safe!" << std::endl;
          ++safe_count;
          break;
        }
      }
    }
    std::cout << std::endl;
  };
  std::cout << safe_count << std::endl;
  return 0;
}
