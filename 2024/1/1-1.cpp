#include <algorithm>
#include <cmath>
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

std::vector<std::string> split(const std::string &input, std::string delimiter) {
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
  std::string number;
  std::vector<int> list_1;
  std::vector<int> list_2;
  int sum;

  while (std::getline(std::cin, line)) {
    std::vector<std::string> items = split(line, "   ");
    list_1.emplace_back(std::stoi(items[0]));
    list_2.emplace_back(std::stoi(items[1]));
  };

  std::sort(list_1.begin(), list_1.end());
  std::sort(list_2.begin(), list_2.end());

  for (size_t i = 0; i < list_1.size(); ++i) {
    sum += std::abs(list_1[i] - list_2[i]);
  }
  std::cout << sum << std::endl;
}
