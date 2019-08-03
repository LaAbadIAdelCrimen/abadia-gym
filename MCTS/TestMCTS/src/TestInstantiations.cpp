#include "../src/MCTS.cpp"
#include "../src/Node.cpp"
#include "Edge.h"

#include "TestState.h"
#include "TestGameState.h"
#include "TestAction.h"

namespace mcts {

template class Node<test_mcts::TestState,test_mcts::TestAction>;
template class Edge<test_mcts::TestState,test_mcts::TestAction>;
template class MCTS<test_mcts::TestState,test_mcts::TestAction>;

template std::ostream& operator<<(std::ostream& os, const Node<test_mcts::TestState,test_mcts::TestAction>& node);


}
