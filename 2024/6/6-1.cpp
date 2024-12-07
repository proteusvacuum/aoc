#include <iostream>
#include <ostream>
#include <set>
#include <vector>

struct Coord {
  int x;
  int y;

  bool operator<(const Coord &other) const {
    if (x != other.x) {
      return x < other.x;
    }
    return y < other.y;
  }
};

struct Velocity {
  int x;
  int y;

  bool operator<(const Velocity &other) const {
    if (x != other.x) {
      return x < other.x;
    }
    return y < other.y;
  }
};

class Board {
public:
  std::set<Coord> obstacles;
  int max_x;
  int max_y;

  Board(std::vector<std::string> &lines) {
    max_x = lines.size();
    max_y = lines[0].size();
    for (int row = 0; row < lines.size(); ++row) {
      for (int column = 0; column < lines[row].size(); ++column) {
        if (lines[row][column] == '#') {
          obstacles.emplace(Coord{column, row});
        }
      }
    }
  }
};

class Guard {
  Coord position;
  Velocity velocity;
  Board board;

public:
  std::set<Coord> visited_positions;
  Guard(std::vector<std::string> &lines, Board &board) : board(board) {
    for (int row = 0; row < lines.size(); ++row) {
      for (int column = 0; column < lines[row].size(); ++column) {
        char current_char = lines[row][column];
        if (current_char == '^') {
          velocity = Velocity{0, -1};
          position = {column, row};
        } else if (current_char == '>') {
          velocity = Velocity{1, 0};
          position = {column, row};
        } else if (current_char == '<') {
          velocity = Velocity{-1, 0};
          position = {column, row};
        } else if (current_char == 'v') {
          velocity = Velocity{0, 1};
          position = {column, row};
        }
      }
    }
  }

  bool inBounds() {
    return (position.x > 0 && position.y > 0 && position.x < board.max_x &&
            position.y < board.max_y);
  }

  bool collision() {
    return (board.obstacles.find(
                Coord{position.x + velocity.x, position.y + velocity.y}) !=
            board.obstacles.end());
  }

  void rotate() {
    int old_x = velocity.x;
    velocity.x = -velocity.y;
    velocity.y = old_x;
  }

  void move() {
    while (collision()) {
      rotate();
    }
    position.x += velocity.x;
    position.y += velocity.y;
    visited_positions.emplace(position);
  }
};

int main() {
  std::string line;
  std::vector<std::string> lines;
  int output = 0;
  while (std::getline(std::cin, line)) {
    lines.emplace_back(line);
  };
  Board board = Board(lines);
  Guard guard = Guard(lines, board);
  while (guard.inBounds()) {
    guard.move();
  };

  std::cout << "visited: " << guard.visited_positions.size() << std::endl;
  return 0;
}
