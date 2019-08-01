#ifndef _MCTS_H
#define _MCTS_H

#include "GeneralTypes.h"

#include <memory>
#include <queue>

namespace mcts {

// template<typename State>
// using CalculateReward = Reward (*)(const State& state);

// template<typename State>
// using CalculateActionProb = Probability (*)(const State& state);

template<typename State,typename Action> class Edge;

template<typename State,typename Action>
struct PossibleMove {
	const Action& 									action;
	const typename State::InternalState 			nextState;
	// const Reward 								reward;
	 Probability									probability;

	PossibleMove(const Action& anAction, const typename State::InternalState& aState, const Probability aProbability) 
		:action(anAction), nextState(aState), probability(aProbability) {}
};

template<typename State,typename Action>
using VectorOfPossibleMoves = std::vector<PossibleMove<State,Action>>;
template<typename State>
using Func_V = Reward (*)(const State& state);
template<typename State,typename Action>
using Func_P = VectorOfPossibleMoves<State,Action> (*)(const State& state);


template<typename State, typename Action> class Node;

template<typename State,typename Action>
class MCTS {
	typedef std::queue<std::shared_ptr<Node<State,Action>>>	Path;

	const size_t					_explorationDepth;
	const size_t					_numMovesToRemember;

	// Node<State,Action>				_root;
	floating_t						_c_puct;
	Func_V<State>					_func_V;
	Func_P<State,Action>			_func_P;

	Node<State,Action>*				_actualNode;

	Path							_path;

	void expandUntilDepth(Node<State,Action>& node, size_t depth);

	void expand(Node<State,Action>& node);
	void backup(Node<State,Action>& node, const Reward& reward);
	const Edge<State,Action>& search(Node<State,Action>& node);

	floating_t moveValue(const Edge<State,Action>& node, unsigned long childrenAccumN) const;

public:
	MCTS(const typename State::InternalState& initialState, floating_t c_puct, Func_V<State> func_V, Func_P<State,Action> func_P,
		const size_t numActions, const size_t explorationDepth, const size_t numMovesToRemember);
	const Action& bestAction();

	bool move(const Action& action);
};

} // namespace mcts

#endif // _MCTS_H