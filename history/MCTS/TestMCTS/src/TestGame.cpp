#include "TestGame.h"

#include "TestMaze.h"
#include "TestPos.h"
#include "TestAction.h"

using namespace test_mcts;
using namespace test_mcts::test_actions;

// static bool operator==(const TestGameState& left, const TestGameState& right) {
//     return (left.actualPos == right.actualPos) && (left.hasKey == right.hasKey);
// }

TestGame::TestGame(const TestMaze& maze): _maze(maze) {
    _gameState.actualPos = maze.getInitialPos();
    _gameState.hasKey = false;
}

bool TestGame::move(const TestAction& action) {
    return move(_gameState, _maze, action);
}

bool TestGame::won() const {
    // const Pos& actualPos(_gameState.actualPos);
    // if(actualPos == _maze.getInitialPos())
    //     return false;
    // else if((_maze.getWidth() - 1 == actualPos.x) || (_maze.getHeight() -1 == actualPos.y))
    //     return true;
    // return false;
    return _gameState.actualPos == _maze.getWinPos();
}

bool TestGame::move(TestGameState& gameState, const TestMaze& maze, const TestAction& action) {
    const bool hasKeyPreviously(gameState.hasKey);
    Pos nextPos(gameState.actualPos);
    if(action == action_N) {
        --nextPos.y;
    } else if(action == action_NE) {
        ++nextPos.x;
        --nextPos.y;
    } else if(action == action_E) {
        ++nextPos.x;
    } else if(action == action_SE) {
        ++nextPos.x;
        ++nextPos.y;
    } else if(action == action_S) {
        ++nextPos.y;
    } else if(action == action_SW) {
        --nextPos.x;
        ++nextPos.y;        
    } else if(action == action_W) {
        --nextPos.x;
    } else if(action == action_NW) {
        --nextPos.x;
        --nextPos.y;
    } else if(action == action_C) {
        
    }
    bool result = (nextPos.x < maze.getWidth()) && (nextPos.y < maze.getHeight());
    if(result) {
        const Cell& cell(maze.getCellAtPos(nextPos));
        result &= !cell.isWall && (gameState.hasKey || !(maze.getGatePos() == nextPos));
    }
    if(result) {
        gameState.actualPos = nextPos;
        gameState.hasKey = hasKeyPreviously || (maze.getKeyPos() == nextPos);
    }
    
    return result;
}
