#ifndef _MCTS_EDGE_H
#define _MCTS_EDGE_H

#include <memory>
#include <cassert>
#include <iostream> //For debuggin purposes only

namespace mcts {

template<typename State,typename Action> class NodeImpl;

template<typename State,typename Action>
class Edge {
	// State and action taken to reach this node
	Node<State,Action>&								_beginNode;
	std::shared_ptr<Node<State,Action>>				_endNodePtr;
	const Action& 									_action;

	Probability										_P;		// Probability of taking this action

public:
	Edge(Node<State,Action>& beginNode, std::shared_ptr<Node<State,Action>>& endNodePtr, const Action& action, const Probability probability)
		:_beginNode(beginNode), _endNodePtr(endNodePtr), _action(action), _P(probability) {
			// std::cout << "Edge created. BeginNode: " << _beginNode.getId() << ", EndNode: " << _endNodePtr->getId() << std::endl;
	}
	~Edge() {
		// std::cout << "Edge destroyed. BeginNode: " << _beginNode.getId() << ", EndNode: " << _endNodePtr->getId() << std::endl;
	}
	// Edge(const Edge& right) :_beginNode(right._beginNode), _endNodePtr(right._endNodePtr), _action(right._action), _P(right._P) {
	// 	std::cout << "Edge create by copy BeginNode: " << _beginNode.getId() << ", EndNode: " << _endNodePtr->getId() << std::endl;
	// }

	// Edge is designed to be immutable, but nodes pointed by it not -> const accessors grant access to mutable nodes.
	// const Node<State,Action>& getBeginNode() const {return _beginNode;}
	Node<State,Action>& getBeginNode() const {return _beginNode;}
	const Node<State,Action>& getEndNode() const {assert(_endNodePtr); return *_endNodePtr;}
	Node<State,Action>& getEndNode() {assert(_endNodePtr); return *_endNodePtr;}
	std::shared_ptr<Node<State,Action>> getEndNodeSPtr() const {return _endNodePtr;}
	const Action& getAction() const {return _action;}

	Probability P() const 	{return _P;}
	// size_t N() const 		{assert(_endNodePtr); return _endNode.N();}
	// Reward W() const	 	{assert(_endNodePtr); return _endNode.W();}
	// Reward Q() const 		{assert(_endNodePtr); return _endNode.Q();}
};

} // namespace mcts

#endif // _MCTS_EDGE_H