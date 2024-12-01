#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

int main() {
  std::string line;
  std::vector<std::string> number_words = {
      "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};
  int total = 0;

  while (std::getline(std::cin, line)) {
    std::vector<std::string> numbers;
    std::string prev_chars = "";
    for (char character : line) {
      if (std::isdigit(character)) {
        std::string num = {character};
        numbers.emplace_back(num);
        prev_chars = "";
      } else {
        prev_chars += {character};
        for (size_t i = 0; i < number_words.size(); ++i) {
          if (prev_chars.find(number_words[i]) != std::string::npos) {
            numbers.emplace_back(std::to_string(i + 1));
            prev_chars =
                prev_chars
                    .back(); // Keep the last character for things like oneight;
          }
        }
      }
    }
    total += std::stoi(numbers.front() + numbers.back());
  }
  std::cout << total << std::endl;
  return 0;
}
