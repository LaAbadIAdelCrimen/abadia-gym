#ifndef _TEST_STATE_H
#define _TEST_STATE_H
 
#include "State.h"
#include "TestGameState.h"
#include "TestPos.h"

#include <memory>
#include <string> //For debugging purpose only

namespace test_mcts {

// class TestStateFactory;

class TestState {
public:
	typedef TestGameState	InternalState;
	// typedef int				IdState;
private:
	// const IdState			_id;
	const InternalState		_internalState;
public:
	// TestState(const IdState id, const InternalState& internalState): _id(id), _internalState(internalState) {}
	TestState(const InternalState& internalState): _internalState(internalState) {}

	const InternalState& getInternalState() const {return _internalState;}

	// IdState getId(const InternalState&) const {return _id;};

	bool operator<(const TestState& right) const;
	// static std::shared_ptr<TestState> getOrCreate(const TestState::InternalState& internalState);

	// Debug info
	std::string getDebugTrace() const;
};

// class TestStateFactory {
// public:
// 	static std::shared_ptr<TestState> getOrCreate(const TestState::InternalState& internalState);
// 	// static TestState& create(const TestState::InternalState& internalState);
// 	// static void remove(const TestState& testState);
// };

}  // namespace test_mcts

#endif //_TEST_STATE_H
