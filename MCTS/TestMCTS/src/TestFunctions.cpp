#include "TestFunctions.h"

#include "TestState.h"
#include "TestGame.h"
#include "TestAction.h"

#include <cmath>
#include <cassert>

using namespace test_mcts;
using namespace mcts;

static const float KEY_WEIGHT = 0.3f;
static const float POS_WEIGHT = 1.0f - KEY_WEIGHT; 

// static size_t WIDTH = 0.0f;
// static size_t HEIGHT = 0.0f;
// static const Pos* WIN_POS = nullptr;
static const TestMaze* MAZE = nullptr;

static float distance(const Pos& pos1, const Pos& pos2) {
    float x = abs(pos2.x - pos1.x);
    float y = abs(pos2.y - pos1.y);
    float result = sqrt(std::pow(x, 2) + std::pow(y, 2));
    return result;
}

// MAZE must be initialized prior to call this function
static float MAX_DISTANCE() {
    static float result = distance(Pos{0u, 0u}, Pos{MAZE->getWidth() - 1, MAZE->getHeight() - 1});
    return result;
}

static void normalizeProbs(VectorOfPossibleMoves<TestState,TestAction>& vectorOfPossibleMoves) {
    Probability accum = 0.0f;
    for(const auto& possibleMove: vectorOfPossibleMoves) {
        if(possibleMove.probability >= 0.0f)
            accum += possibleMove.probability;
    }
    assert(accum >= 0.0f);
    for(auto& possibleMove: vectorOfPossibleMoves) {
        if(possibleMove.probability >= 0.0f)
            possibleMove.probability = (accum == 0.0f) ? 0.0f : possibleMove.probability / accum;
    }
}

namespace test_mcts {

void initialize(const TestMaze& maze) {
    MAZE = &maze;
}

Reward reward(const TestState& state) {
    assert(MAZE != nullptr);
    const TestState::InternalState& internalState(state.getInternalState());
    Reward result = (internalState.hasKey ? 1.0f : 0.0f) * KEY_WEIGHT + (1.0f - distance(internalState.actualPos, MAZE->getWinPos()) / MAX_DISTANCE()) * POS_WEIGHT;
    return result;
}

VectorOfPossibleMoves<TestState,TestAction> moveProbabilities(const TestState& state) {
    const test_actions::Actions& actions(test_actions::getActions());
    VectorOfPossibleMoves<TestState,TestAction> result;
    for(const TestAction* action :actions) {
        assert(action != nullptr);
        TestGameState gameState(state.getInternalState());
        const bool isValidMove(TestGame::move(gameState, *MAZE, *action));
        const Probability prob(isValidMove ? 1.0f - distance(gameState.actualPos, MAZE->getWinPos()) / MAX_DISTANCE() : -1.0f);
        result.emplace_back(*action, gameState, prob);
    }
    normalizeProbs(result);
    return result;
}

} // namespace test_mcts