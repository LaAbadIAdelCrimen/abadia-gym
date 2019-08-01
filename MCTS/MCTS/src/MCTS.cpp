// MCTS.cpp : Defines the entry point for the console application.
//

#include "MCTS.h"

#include "Node.h"
#include "Edge.h"
// #include "TestGameState.h"

#include <cmath>
#include <queue>
#include <algorithm>
#include <cassert>

#include <iostream>

using namespace std;
using namespace mcts;

template<typename State,typename Action>
MCTS<State,Action>::MCTS(const typename State::InternalState& initialState, floating_t c_puct, Func_V<State> func_V, Func_P<State,Action> func_P,
	const size_t numActions, const size_t explorationDepth, const size_t numMovesToRemember) 
		:_c_puct(c_puct), _func_V(func_V), _func_P(func_P), _explorationDepth(explorationDepth), _numMovesToRemember(numMovesToRemember) {
	NodeFactory<State,Action>::setNumActions(numActions);
	std::shared_ptr<Node<State,Action>> nodePtr = NodeFactory<State,Action>::getOrCreate(initialState);
	_path.push(nodePtr);
	_actualNode = nodePtr.get();

}

template<typename State,typename Action>
void MCTS<State,Action>::expandUntilDepth(Node<State,Action>& node, const size_t depth) {
	if(0 == depth) return;
    typename Node<State,Action>::NextMoves& nextMoves(node.getNextMoves());
	if(nextMoves.empty())
		expand(node);
    for(auto& edge: nextMoves) {
		if(edge.P() > -1.0) {
			Node<State,Action>& endNode(edge.getEndNode());
			expandUntilDepth(endNode, depth - 1);
		}
    }
}

template<typename State,typename Action>
void MCTS<State,Action>::expand(Node<State,Action>& node) {
	assert(node.getNextMoves().empty());
	const Reward reward(_func_V(node.getState()));
	VectorOfPossibleMoves<State,Action> possibleMoves(_func_P(node.getState()));
	for(auto& possibleMove: possibleMoves) {
		// std::shared_ptr<State> nextState(State::getOrCreate(possibleMove.nextState));
		node.addNextMove(possibleMove.nextState, possibleMove.action, possibleMove.probability);
	}
	backup(node, reward);
}

template<typename State,typename Action>
void MCTS<State,Action>::backup(Node<State,Action>& node, const Reward& reward) {
	// for(auto it = _path.rbegin(); it != _path.rend(); ++it) {
	// 	Node<State,Action>& node(**it);
	// 	node.update(w);
	// }
	Node<State,Action>* actualNode = &node;
	while(actualNode) {
		actualNode->update(reward);
		const Edge<State,Action>* priorMove = actualNode->getPriorMove();
		if(priorMove)
			actualNode = &priorMove->getBeginNode();
		else
			actualNode = nullptr;
	}
}

// Puct formula
// s -> state, a -> action, b -> each action in sumatorio
// U(s,a) = c_puct * P(s,a) * sqrt(Sumatorio_b(N(s,b) / (1 + N(s,a))
// moveValue = Q(s,a) + u(s,a)
// childrenAccumN parameter is Sumatorio_b(N_b)
template<typename State,typename Action>
floating_t MCTS<State,Action>::moveValue(const Edge<State,Action>& edge, unsigned long childrenAccumN) const {
	const Node<State,Action>& childNode(edge.getEndNode());
	float u = _c_puct * edge.P() * std::sqrt(childrenAccumN / (1 + childNode.N()));
	float result = childNode.Q() + u;
	return result;
}

template<typename State,typename Action>
const Edge<State,Action>& MCTS<State,Action>::search(Node<State,Action>& node) {
	typedef std::pair<float, const Edge<State,Action>*> MoveValue;
	static const MoveValue DEFAULT_MOVE_VALUE {0.0f, nullptr};
	expandUntilDepth(node, _explorationDepth);
	const typename Node<State,Action>::NextMoves& children(node.getNextMoves());
	// assert(children != nullptr);
	// if(children->empty()) {
	// 	//TODO: Think about constness with Node, Edge, ...
	// 	expand(node);
	// 	children = &node.getNextMoves();
	// 	assert(children != nullptr);
	// }
	assert(!children.empty());
	size_t childrenAccumN = 0;
	for(auto& childEdge: children) {
		const Node<State,Action>& childNode(childEdge.getEndNode());
		childrenAccumN += childNode.N();
	}
	std::vector<MoveValue> moveValues(children.size(), DEFAULT_MOVE_VALUE);
	if(childrenAccumN)
		std::transform(children.begin(), children.end(), moveValues.begin(), 
			[=](const Edge<State,Action>& childEdge) -> MoveValue {return std::make_pair(moveValue(childEdge, childrenAccumN), &childEdge);});
	else
		std::transform(children.begin(), children.end(), moveValues.begin(), 
			[=](const Edge<State,Action>& childEdge) -> MoveValue {return std::make_pair(childEdge.P(), &childEdge);});

	auto maxValueIt = std::max_element(moveValues.begin(), moveValues.end(), 
		[](const MoveValue& left, const MoveValue& right) -> bool {return left.first < right.first;});
	assert(maxValueIt != moveValues.end());
	assert(maxValueIt->first >= 0);
	_actualNode = &node;
	return *maxValueIt->second;
}

template<typename State,typename Action>
const Action& MCTS<State,Action>::bestAction() {
	const Edge<State,Action>& edge(search(*_actualNode));
	const Action& action(edge.getAction());
	std::shared_ptr<Node<State,Action>> node(edge.getEndNodeSPtr());
	return action;
}

template<typename State,typename Action>
bool MCTS<State,Action>::move(const Action& action) {
	assert(_actualNode != nullptr);
	// std::cout << *_actualNode;
	typename Node<State,Action>::NextMoves& nextMoves = _actualNode->getNextMoves();
	auto edgeIt(std::find_if(nextMoves.begin(), nextMoves.end(), [&action](const Edge<State,Action>& edge) {return edge.getAction() == action;}));
	if(edgeIt == nextMoves.end())
		return false;
	Node<State,Action>& nextNode(edgeIt->getEndNode());
	_actualNode = &nextNode;
	_path.push(edgeIt->getEndNodeSPtr());
	if(_numMovesToRemember < _path.size())
		_path.pop();
	assert(_actualNode != nullptr);
	return true;
}
