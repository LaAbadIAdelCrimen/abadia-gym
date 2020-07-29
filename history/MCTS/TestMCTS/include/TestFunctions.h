#ifndef _TEST_FUNCTIONS_H
#define _TEST_FUNCTIONS_H

#include "MCTS.h"

namespace test_mcts {

class TestMaze;
class TestState;
class TestAction;
class InternalState;
struct Pos;

void initialize(const TestMaze& maze);

mcts::Reward reward(const TestState& state);

mcts::VectorOfPossibleMoves<TestState,TestAction> moveProbabilities(const TestState& state);

} // namespace test_mcts

#endif //_TEST_FUNCITONS_H