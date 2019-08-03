#ifndef _TEST_GAME_H
#define _TEST_GAME_H

#include "TestMaze.h"
#include "TestGameState.h"

#include <iosfwd>

namespace test_mcts {

class TestAction;
class TestMaze;

class TestGame {
    const TestMaze&     _maze;
    TestGameState       _gameState;
public:
    TestGame(const TestMaze& maze);

    const TestGameState& getGameState() const {return _gameState;}

    bool move(const TestAction& action);

    bool won() const;

    static bool move(TestGameState& gameState, const TestMaze& maze, const TestAction& action);

    friend std::ostream& operator<<(std::ostream& os, const TestGame& game);
};

} //namespace test_mcts

#endif //_TEST_GAME_H