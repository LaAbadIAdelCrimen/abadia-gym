#ifndef _TEST_ACTION_H
#define _TEST_ACTION_H

#include "Action.h"

#include <string>
#include <vector>
#include <assert.h>

namespace test_mcts {

class TestAction {
	std::string	_name;

public:
	TestAction(const TestAction&) = delete;
	TestAction& operator=(const TestAction&) = delete;
	explicit TestAction(const std::string& name): _name(name) {}
	explicit TestAction(std::string&& name): _name(name) {}

	bool operator==(const TestAction& other) const {return &other == this;}

	const std::string& getName() const {return _name;}
};

namespace test_actions {
	typedef std::vector<const TestAction*> Actions;
	// const TestAction action_N("N");
	// const TestAction action_NE("NE");
	// const TestAction action_E("E");
	// const TestAction action_SE("SE");
	// const TestAction action_S("S");
	// const TestAction action_SW("SW");
	// const TestAction action_W("W");
	// const TestAction action_NW("NW");
	// const TestAction action_C("C");
	extern const TestAction action_N;
	extern const TestAction action_NE;
	extern const TestAction action_E;
	extern const TestAction action_SE;
	extern const TestAction action_S;
	extern const TestAction action_SW;
	extern const TestAction action_W;
	extern const TestAction action_NW;
	extern const TestAction action_C;
	extern const Actions& getActions();
}

} // namespace test_mcts

#endif //_TEST_ACTION_H