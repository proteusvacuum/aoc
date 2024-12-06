#include <algorithm>
#include <iostream>
#include <iterator>
#include <regex>
#include <string>
#include <tuple>

using std::cout;
using std::string;

std::vector<string> split(const string &input, const string &delimiter) {
  std::vector<string> tokens;
  size_t start = 0;
  size_t end = input.find(delimiter);

  while (end != string::npos) {
    tokens.push_back(input.substr(start, end - start));
    start = end + delimiter.size();
    end = input.find(delimiter, start);
  }

  tokens.push_back(input.substr(start));
  return tokens;
};

void parseRules(string &line, std::map<int, std::vector<int>> &before,
                std::map<int, std::vector<int>> &after) {
  auto split_line = split(line, "|");
  int before_item = std::stoi(split_line.front());
  int after_item = std::stoi(split_line.back());
  before[before_item].emplace_back(after_item);
  after[after_item].emplace_back(before_item);
}

void parseUpdate(string &line, std::vector<std::vector<int>> &updates) {
  std::vector<string> split_line = split(line, ",");
  std::vector<int> int_line;
  for (const auto &s : split_line) {
    int_line.push_back(std::stoi(s));
  }
  updates.emplace_back(int_line);
}

bool checkUpdate(const std::vector<int> &update,
                 std::map<int, std::vector<int>> &before,
                 std::map<int, std::vector<int>> &after) {
  for (const auto &item : update) {
    auto item_index = std::distance(
        update.begin(), std::find(update.begin(), update.end(), item));
    for (const auto &before_item : before[item]) {
      auto before_index = std::distance(
          update.begin(), std::find(update.begin(), update.end(), before_item));
      bool item_in_update = before_index < update.size();
      if (item_in_update && before_index < item_index) {
        return false;
      }
    }
    for (const auto &after_item : after[item]) {
      auto after_index = std::distance(
          update.begin(), std::find(update.begin(), update.end(), after_item));
      bool item_in_update = after_index < update.size();
      if (item_in_update && after_index > item_index) {
        return false;
      }
    }
  }
  return true;
}

int getMiddleItem(const std::vector<int> &update) {
  return update[update.size() / 2];
}

bool compareUpdates(const int &item1, const int &item2,
                    std::map<int, std::vector<int>> &before) {
  return (std::find(before[item1].begin(), before[item1].end(), item2) != before[item1].end());
}

void reorderUpdate(std::vector<int>& update, std::map<int, std::vector<int>> &before) {
  auto sortFn = [&before](const int& item1, const int& item2){
    return compareUpdates(item1, item2, before);
  };

  std::sort(update.begin(), update.end(), sortFn);
}

void printUpdate(std::vector<std::vector<int>>& updates){
  for (auto &update : updates) {
    for (auto &num : update) {
      cout << num << ", ";
    }
    cout << std::endl;
  }
}

int main() {
  int output = 0;
  string line;

  std::map<int, std::vector<int>> before;
  std::map<int, std::vector<int>> after;

  std::vector<std::vector<int>> updates;
  bool parsing_rules = true;
  while (std::getline(std::cin, line)) {
    if (line.size() == 0) {
      parsing_rules = false;
      continue;
    }
    if (parsing_rules) {
      parseRules(line, before, after);
    } else {
      parseUpdate(line, updates);
    }
  };

  for (auto &update : updates) {
    if (!checkUpdate(update, before, after)) {
      reorderUpdate(update, before);
      output += getMiddleItem(update);
    }
  }

  cout << output << std::endl;
  return 0;
}
