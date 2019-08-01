#include "TestState.h"

// #include <memory>
// #include <map>
#include <cassert>

using namespace test_mcts;
using namespace std;

bool TestState::operator<(const TestState& rightState) const {
    const InternalState& left(getInternalState());
    const InternalState& right(rightState.getInternalState());
    // assert(left != nullptr);
    // assert(right != nullptr);
    return (left.actualPos.x < right.actualPos.x) ||
            ((left.actualPos.x == right.actualPos.x) && (left.actualPos.y < right.actualPos.y)) ||
            ((left.actualPos == right.actualPos) && (left.hasKey < right.hasKey));
}

std::string TestState::getDebugTrace() const {
    const InternalState& intState(getInternalState());
    const Pos& pos(intState.actualPos);
    std::string result = std::string("Pos(") + std::to_string(pos.x) + "," + std::to_string(pos.y) + "). hasKey=" + to_string(intState.hasKey);
    return result;
}

// struct LessTestGameStatePtr {
//     bool operator() (const TestGameState* left, const TestGameState* right) const {
//         assert(left != nullptr);
//         assert(right != nullptr);
//         return (left->actualPos.x < right->actualPos.x) ||
//                 ((left->actualPos.x == right->actualPos.x) && (left->actualPos.y < right->actualPos.y)) ||
//                 ((left->actualPos == right->actualPos) && (left->hasKey < right->hasKey));
//     }
// };


// namespace test_mcts {

// // TestStateFactory
// class TestStateFactoryImpl {
// public:
//     typedef map<const TestState::InternalState*, weak_ptr<TestState>, LessTestGameStatePtr>         StatesByInternalState;
// private:
//     static TestState::IdState           _counter;
//     static StatesByInternalState        _aliveStates;
// public:
// 	static shared_ptr<TestState> getOrCreate(const TestState::InternalState& internalState) {
//         auto testStateIt = _aliveStates.find(&internalState);
//         if(testStateIt == _aliveStates.end()) {     //If internalState is not registered
//             shared_ptr<TestState> sptrState(new TestState(_counter++, internalState), &TestStateFactoryImpl::remove);
//             auto insertResult = _aliveStates.insert(StatesByInternalState::value_type(&internalState, weak_ptr<TestState>(sptrState)));
//             assert(insertResult.second == true);
//             return sptrState;
//         } else {
//             assert(testStateIt->second.expired() == false);
//             shared_ptr<TestState> sptrState(testStateIt->second.lock());
//             return sptrState;
//         }
//     }
//     static void remove(TestState* toRemove) {
//         assert(toRemove != nullptr);
//         const TestState::InternalState* internalState(&toRemove->getInternalState());
//         _aliveStates.erase(internalState);
//         delete toRemove;
//     }
// };
// TestState::IdState TestStateFactoryImpl::_counter = TestState::IdState();
// TestStateFactoryImpl::StatesByInternalState TestStateFactoryImpl::_aliveStates;
    

// std::shared_ptr<TestState> TestStateFactory::getOrCreate(const TestState::InternalState& internalState) {
//     return TestStateFactoryImpl::getOrCreate(internalState);
// }

// std::shared_ptr<TestState> TestState::getOrCreate(const TestState::InternalState& internalState) {return TestStateFactory::getOrCreate(internalState);}

// } // namespace test_mcts
