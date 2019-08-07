#include "TestAction.h"
#include <cstdlib>

using namespace test_mcts;

// NW  N  NE
// W   C   E
// SW  S  SE
namespace test_mcts {
	namespace test_actions {
		const TestAction action_N("N");
		const TestAction action_NE("NE");
		const TestAction action_E("E");
		const TestAction action_SE("SE");
		const TestAction action_S("S");
		const TestAction action_SW("SW");
		const TestAction action_W("W");
		const TestAction action_NW("NW");
		const TestAction action_C("C");

		const Actions& getActions() {
			static Actions actions {
				&action_N,
				&action_NE,
				&action_E,
				&action_SE,
				&action_S,
				&action_SW,
				&action_W,
				&action_NW,
				&action_C
			};
			return actions;
		}
	} // namespace test_actions
} // namespace test_mcts

