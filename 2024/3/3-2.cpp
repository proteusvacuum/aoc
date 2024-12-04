#include <deque>
#include <iostream>
#include <iterator>
#include <regex>
#include <string>

int main() {
  std::string line;
  long long output;
  bool enabled = true;
  std::regex do_regex("do\\(\\)");
  std::regex dont_regex("don't\\(\\)");
  std::regex mul_regex("mul\\((\\d{1,3}),(\\d{1,3})\\)");
  std::deque<int> do_positions;
  std::deque<int> dont_positions;
  int current_do_pos;
  int current_dont_pos;

  while (std::getline(std::cin, line)) {
    if (enabled){
      do_positions = {-1};
      dont_positions = {-2};
    } else {
      do_positions = {-2};
      dont_positions = {-1};
    }

    auto end = std::sregex_iterator();
    auto dos = std::sregex_iterator(line.begin(), line.end(), do_regex);
    auto donts = std::sregex_iterator(line.begin(), line.end(), dont_regex);
    for (std::sregex_iterator i = dos; i != end; ++i) {
      std::smatch match = *i;
      std::string mul_str = match.str();
      do_positions.emplace_back(match.position());
    };

    for (std::sregex_iterator i = donts; i != end; ++i) {
      std::smatch match = *i;
      std::string mul_str = match.str();
      dont_positions.emplace_back(match.position());
    };

    std::cout << "Dos: (";
    for (auto pos : do_positions){
      std::cout << pos << ", ";
    }
    std::cout << ")" << std::endl;
    std::cout << "Donts: (";
    for (auto pos : dont_positions) {
      std::cout << pos << ", ";
    }
    std::cout << ")" << std::endl;

    current_do_pos = do_positions.front();
    do_positions.pop_front();
    current_dont_pos = dont_positions.front();
    dont_positions.pop_front();

    auto muls = std::sregex_iterator(line.begin(), line.end(), mul_regex);
    for (std::sregex_iterator i = muls; i != end; ++i) {
      std::smatch match = *i;
      std::string mul_str = match.str();
      std::cout << "---" << std::endl;
      std::cout << "Match position: " << match.position() << std::endl;
      std::cout << match.str() << std::endl;

      if (!do_positions.empty() && match.position() > do_positions.front()) {
        current_do_pos = do_positions.front();
        do_positions.pop_front();
      }
      if (!dont_positions.empty() && match.position() > dont_positions.front()) {
        current_dont_pos = dont_positions.front();
        dont_positions.pop_front();
      }

      std::cout << "do: " << current_do_pos << std::endl;
      std::cout << "dont: " << current_dont_pos << std::endl;

      if (match.position() > current_do_pos &&
          current_do_pos > current_dont_pos) {
        output += std::stoi(match[1].str()) * std::stoi(match[2].str());
        std::cout << "match: " << match[1] << ", " << match[2]
                  << "=" << std::stoi(match[1].str()) * std::stoi(match[2].str())
                  << "  Output: " << output
                  << std::endl;
      }
      std::cout << std::endl;
    };
    enabled = current_do_pos > current_dont_pos;
    std::cout << "line ends with do: " << enabled << std::endl;
  };
  std::cout << output << std::endl;
}
