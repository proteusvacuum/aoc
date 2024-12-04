#include <iostream>
#include <iterator>
#include <regex>
#include <string>

int main() {
  std::string line;
  int output;
  std::regex mul_regex("mul\\((\\d{1,3}),(\\d{1,3})\\)");
  while (std::getline(std::cin, line)){
    auto muls = std::sregex_iterator(line.begin(), line.end(), mul_regex);
    auto muls_end = std::sregex_iterator();
    for (std::sregex_iterator i = muls; i != muls_end; ++i) {
      std::smatch match = *i;
      std::string mul_str = match.str();
      output += std::stoi(match[1].str()) * std::stoi(match[2].str());
    };
  };
  std::cout << output << std::endl;
}
