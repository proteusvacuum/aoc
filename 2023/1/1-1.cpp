#include <algorithm>
#include <iostream>
#include <string>

int main() {
  std::string line;
  std::string number;
  int total = 0;
  while (std::getline(std::cin, line)) {
    for (char character : line) {
      if (std::isdigit(character)) {
        number = character;
        break;
      }
    }
    std::reverse(line.begin(), line.end());

    for (char character : line) {
      if (std::isdigit(character)) {
        number += character;
        break;
      }
    }
    total += std::stoi(number);
  }
  std::cout << total;
  return 0;
}
