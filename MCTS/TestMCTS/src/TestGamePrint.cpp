#include "TestGamePrint.h"

#include "TestMaze.h"
#include "TestGame.h"
#include "TestGameState.h"

#include <ostream>

namespace test_mcts {

// Printable output 
std::ostream& operator<<(std::ostream& os, const TestGame& game) {
    static const char WALL = 'W';

    const TestMaze& maze(game._maze);
    const TestGameState& gameState = game.getGameState();
    const Pos& actualPos = gameState.actualPos;
    const bool hasKey = gameState.hasKey;
    const Pos& keyPos = maze.getKeyPos();
    const Pos& gatePos = maze.getGatePos();


    const TestMaze::MazeDefinition& mazeDefinition(maze.getDefinition());
    const size_t width = maze.getWidth();
    const size_t height = maze.getHeight();
    for(size_t y = 0; y < height; ++y) {
        std::string line(width + 1, '\0');
        for(size_t x = 0; x < width; ++x) {
            size_t offset = y * width + x;
            const Cell& cell(mazeDefinition[offset]);
            char posRepr = '\0';
            if(cell.isWall)
                posRepr = WALL;
            else if((actualPos.x == x) && (actualPos.y == y)) {
                if(hasKey)
                    posRepr = 'P';
                else
                    posRepr = 'p';               
            } else if((keyPos.x == x) && (keyPos.y == y)) {
                if(hasKey)
                    posRepr = ' ';
                else
                    posRepr = 'K';
            } else if((gatePos.x == x) && (gatePos.y == y))
                posRepr = 'G';
            else
                posRepr = ' ';
            line[x] = posRepr;
        }
        os << line << std::endl;
    }
    return os;
}

} // namespace test_mcts;
