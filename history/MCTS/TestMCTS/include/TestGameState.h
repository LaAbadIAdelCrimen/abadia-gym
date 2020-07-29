#ifndef _TEST_GAME_STATE_H
#define _TEST_GAME_STATE_H

#include "TestPos.h"

namespace test_mcts {

struct TestGameState {
    Pos         actualPos;
    bool        hasKey;
};

}   // namespace test_mcts

#endif //_TEST_GAME_STATE_H