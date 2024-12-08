#include <algorithm>
#include <iostream>
#include <ostream>
#include <set>
#include <stdexcept>
#include <vector>

class LoopError : public std::runtime_error {
public:
  explicit LoopError(const char *message) : std::runtime_error(message) {}
};

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
  Velocity velocity;
  Board board;

public:
  Coord position;
  std::set<Coord> visited_positions;
  std::set<std::pair<Coord, Velocity>> visited_position_directions;
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
    visited_position_directions.emplace(
        std::pair<Coord, Velocity>{position, velocity});
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
    if (visited_position_directions.find(std::pair<Coord, Velocity>{
            position, velocity}) != visited_position_directions.end()) {
      throw LoopError("Loop found");
    }
    visited_positions.emplace(position);
    visited_position_directions.emplace(
        std::pair<Coord, Velocity>{position, velocity});
  }
};

std::set<Coord> getPossibleObstacles(std::vector<std::string> &lines) {
  Board board = Board(lines);
  Guard guard = Guard(lines, board);
  Coord initial_position = {guard.position.x, guard.position.y};
  while (guard.inBounds()) {
    guard.move();
  };
  std::set<Coord> visited_positions;
  for (auto &visited_position_direction : guard.visited_position_directions) {
    visited_positions.emplace(visited_position_direction.first);
  }
  visited_positions.erase(initial_position);
  return visited_positions;
}

bool processNewObstacle(Coord obstacle, std::vector<std::string> &lines) {
  Board board = Board(lines);
  board.obstacles.emplace(obstacle);
  Guard guard = Guard(lines, board);
  Coord initial_position = {guard.position.x, guard.position.y};
  while (guard.inBounds()) {
    try {
      guard.move();
    } catch (const LoopError &e) {
      return true;
    }
  };
  return false;
}

int main() {
  std::string line;
  std::vector<std::string> lines;
  int output = 0;
  while (std::getline(std::cin, line)) {
    lines.emplace_back(line);
  };
  std::set<Coord> new_obstacles = getPossibleObstacles(lines);
  for (const Coord &new_obstacle : new_obstacles) {
    if (processNewObstacle(new_obstacle, lines)) {
      output++;
    }
  }

  std::cout << output << std::endl;
  return 0;
}
