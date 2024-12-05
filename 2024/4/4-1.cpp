#include <iostream>
#include <iterator>
#include <regex>
#include <string>
#include <tuple>

int main() {
  std::string line;
  int output = 0;

  std::vector<std::vector<char>> board;

  struct position {
    int row;
    int column;
  };

  std::vector<position> x_positions;
  int row = 0;
  int column = 0;

  while (std::getline(std::cin, line)) {
    std::vector<char> row_vec;
    for (char letter : line) {
      row_vec.emplace_back(letter);
      if (letter == 'X') {
        x_positions.emplace_back(position{row, column});
      }
      ++column;
    }
    board.emplace_back(row_vec);
    ++row;
    column = 0;
  };

  // std::cout << "Board:" << std::endl;
  // for (const auto &row_vec : board) {
  //   for (char c : row_vec) {
  //     std::cout << c << " ";
  //   }
  //   std::cout << std::endl;
  // }

  // std::cout << x_positions.size() << " Positions of 'X':" << std::endl;
  // for (const auto &pos : x_positions) {
  //   std::cout << "Row: " << pos.row << ", Column: " << pos.column <<
  //   std::endl;
  // }

  for (position x_pos : x_positions) {
    // down:
    if (x_pos.row + 1 < board.size() &&
        board[x_pos.row + 1][x_pos.column] == 'M') {
      if (x_pos.row + 2 < board.size() &&
          board[x_pos.row + 2][x_pos.column] == 'A') {
        if (x_pos.row + 3 < board.size() &&
            board[x_pos.row + 3][x_pos.column] == 'S') {
          output++;
        }
      }
    }
    // up:
    if (x_pos.row - 1 >= 0 && board[x_pos.row - 1][x_pos.column] == 'M') {
      if (x_pos.row - 2 >= 0 && board[x_pos.row - 2][x_pos.column] == 'A') {
        if (x_pos.row - 3 >= 0 && board[x_pos.row - 3][x_pos.column] == 'S') {
          output++;
        }
      }
    }

    // Left check
    if (x_pos.column - 1 >= 0 && board[x_pos.row][x_pos.column - 1] == 'M') {
      if (x_pos.column - 2 >= 0 && board[x_pos.row][x_pos.column - 2] == 'A') {
        if (x_pos.column - 3 >= 0 &&
            board[x_pos.row][x_pos.column - 3] == 'S') {
          output++;
        }
      }
    }

    // Right check
    if (x_pos.column + 1 < board[x_pos.row].size() &&
        board[x_pos.row][x_pos.column + 1] == 'M') {
      if (x_pos.column + 2 < board[x_pos.row].size() &&
          board[x_pos.row][x_pos.column + 2] == 'A') {
        if (x_pos.column + 3 < board[x_pos.row].size() &&
            board[x_pos.row][x_pos.column + 3] == 'S') {
          output++;
        }
      }
    }

    // Top-left diagonal
    if (x_pos.row - 1 >= 0 && x_pos.column - 1 >= 0 &&
        board[x_pos.row - 1][x_pos.column - 1] == 'M') {
      if (x_pos.row - 2 >= 0 && x_pos.column - 2 >= 0 &&
          board[x_pos.row - 2][x_pos.column - 2] == 'A') {
        if (x_pos.row - 3 >= 0 && x_pos.column - 3 >= 0 &&
            board[x_pos.row - 3][x_pos.column - 3] == 'S') {
          output++;
        }
      }
    }

    // Top-right diagonal
    if (x_pos.row - 1 >= 0 && x_pos.column + 1 < board[x_pos.row].size() &&
        board[x_pos.row - 1][x_pos.column + 1] == 'M') {
      if (x_pos.row - 2 >= 0 && x_pos.column + 2 < board[x_pos.row].size() &&
          board[x_pos.row - 2][x_pos.column + 2] == 'A') {
        if (x_pos.row - 3 >= 0 && x_pos.column + 3 < board[x_pos.row].size() &&
            board[x_pos.row - 3][x_pos.column + 3] == 'S') {
          output++;
        }
      }
    }

    // Bottom-left diagonal
    if (x_pos.row + 1 < board.size() && x_pos.column - 1 >= 0 &&
        board[x_pos.row + 1][x_pos.column - 1] == 'M') {
      if (x_pos.row + 2 < board.size() && x_pos.column - 2 >= 0 &&
          board[x_pos.row + 2][x_pos.column - 2] == 'A') {
        if (x_pos.row + 3 < board.size() && x_pos.column - 3 >= 0 &&
            board[x_pos.row + 3][x_pos.column - 3] == 'S') {
          output++;
        }
      }
    }

    // Bottom-right diagonal
    if (x_pos.row + 1 < board.size() &&
        x_pos.column + 1 < board[x_pos.row].size() &&
        board[x_pos.row + 1][x_pos.column + 1] == 'M') {
      if (x_pos.row + 2 < board.size() &&
          x_pos.column + 2 < board[x_pos.row].size() &&
          board[x_pos.row + 2][x_pos.column + 2] == 'A') {
        if (x_pos.row + 3 < board.size() &&
            x_pos.column + 3 < board[x_pos.row].size() &&
            board[x_pos.row + 3][x_pos.column + 3] == 'S') {
          output++;

        }
      }
    }
  }
  std::cout << output << std::endl;
};
