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

int main() {
  std::string line;
  int safe_count = 0;
  while (std::getline(std::cin, line)) {
    std::vector<std::string> items = split(line, " ");
    bool safe = true;
    bool prev_decreasing = (std::stoi(items[0]) - std::stoi(items[1])) < 0;
    for (int i = 0; i < items.size() - 1; ++i) {
      int first_item = std::stoi(items[i]);
      int second_item = std::stoi(items[i + 1]);
      bool decreasing = (first_item - second_item) < 0;
      std::cout << second_item << "-" << first_item << " = "
                << std::abs(second_item - first_item);
      if (std::abs(second_item - first_item) > 3 || second_item == first_item || prev_decreasing != decreasing) {
        std::cout << " unsafe!";
        safe = false;
      }
      std::cout << std::endl;
      prev_decreasing = decreasing;
    }
    if (safe) {
      ++safe_count;
    }
    std::cout << std::endl;
  };
  std::cout << safe_count << std::endl;
  return 0;
}
