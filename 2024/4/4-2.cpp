#include <algorithm>
#include <iostream>
#include <iterator>
#include <regex>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>

int main() {
  std::string line;
  int output = 0;

  std::vector<std::vector<char>> board;

  struct position {
    int row;
    int column;

    bool operator==(const position& other) const {
      return row == other.row && column == other.column;
    }
  };

  std::vector<position> m_positions;
  int row = 0;
  int column = 0;

  while (std::getline(std::cin, line)) {
    std::vector<char> row_vec;
    for (char letter : line) {
      row_vec.emplace_back(letter);
      if (letter == 'M') {
        m_positions.emplace_back(position{row, column});
      }
      ++column;
    }
    board.emplace_back(row_vec);
    ++row;
    column = 0;
  };

  // If this is a match, they have the same position of their A
  std::vector<std::pair<int, int>> a_pos;

  for (const position& m_pos : m_positions) {
    // Top-left diagonal
    if (m_pos.row - 1 >= 0 && m_pos.column - 1 >= 0 &&
        board[m_pos.row - 1][m_pos.column - 1] == 'A') {
      if (m_pos.row - 2 >= 0 && m_pos.column - 2 >= 0 &&
          board[m_pos.row - 2][m_pos.column - 2] == 'S') {
        position pos = {m_pos.row - 1, m_pos.column - 1};
        a_pos.emplace_back(pos.row, pos.column);
      }
    }

    // Top-right diagonal
    if (m_pos.row - 1 >= 0 && m_pos.column + 1 < board[m_pos.row].size() &&
        board[m_pos.row - 1][m_pos.column + 1] == 'A') {
      if (m_pos.row - 2 >= 0 && m_pos.column + 2 < board[m_pos.row].size() &&
          board[m_pos.row - 2][m_pos.column + 2] == 'S') {
        position pos = {m_pos.row - 1, m_pos.column + 1};
        a_pos.emplace_back(pos.row, pos.column);
      }
    }

    // Bottom-left diagonal
    if (m_pos.row + 1 < board.size() && m_pos.column - 1 >= 0 &&
        board[m_pos.row + 1][m_pos.column - 1] == 'A') {
      if (m_pos.row + 2 < board.size() && m_pos.column - 2 >= 0 &&
          board[m_pos.row + 2][m_pos.column - 2] == 'S') {
        position pos = {m_pos.row + 1, m_pos.column - 1};
        a_pos.emplace_back(pos.row, pos.column);
      }
    }

    // Bottom-right diagonal
    if (m_pos.row + 1 < board.size() &&
        m_pos.column + 1 < board[m_pos.row].size() &&
        board[m_pos.row + 1][m_pos.column + 1] == 'A') {
      if (m_pos.row + 2 < board.size() &&
          m_pos.column + 2 < board[m_pos.row].size() &&
          board[m_pos.row + 2][m_pos.column + 2] == 'S') {
        position pos = {m_pos.row + 1, m_pos.column + 1};
        a_pos.emplace_back(pos.row, pos.column);
      }
    }
  }

  std::map<std::pair<int, int>, int> position_count;
  for (const auto& pos : a_pos) {
    position_count[pos]++;
  }
  for (const auto& entry : position_count) {
    if (entry.second == 2){ ++output; }
  }
  std::cout << output << std::endl;
};
