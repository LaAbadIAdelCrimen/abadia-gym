#ifndef _MCTS_NODE_H
#define _MCTS_NODE_H

// Notas:
// 1. En los juegos de la implementaci�n de mcts que he visto, un estado no se puede repetir. Aqu�, sin embargo, se puede llegar al mismo estado por distintos caminos.
//		Inicialmente vamos a considerar que el mismo estado al que se ha llegado por distintos caminos produce distintos nodos.
// 2. Inicialmente usaremos otra distribuci�n (y no dirichlet) para la generaci�n de aleatorios, al menos hasta que encontremos una implementaci�n.

#include "GeneralTypes.h"

#include <vector>
#include <memory>

namespace mcts {

template<typename State,typename Action> class Edge;

template<typename State,typename Action> class NodeFactory;
template<typename State,typename Action> class NodeFactoryImpl;

template<typename State,typename Action>
class NodeImpl;


//tengo que meter el mutex en NodeImpl y poner los accesores y modificadores para que bloqueen el NodeImpl
template<typename State,typename Action>
class Node {
	friend class NodeFactoryImpl<State,Action>;
public:
	typedef const Edge<State,Action>*           		PriorMove;
	typedef std::vector<Edge<State,Action>> 			NextMoves;
private:
	size_t										_id;
	std::shared_ptr<NodeImpl<State,Action>>		_nodeImpl;
	PriorMove									_priorMove;
	NextMoves									_nextMoves;

	// Construct only from NodeFactory
	Node(const size_t id, std::shared_ptr<NodeImpl<State,Action>>&& nodeImpl, const size_t numActions);

	Node(const Node<State,Action>& src) = delete;
	Node<State,Action>& operator=(const Node<State,Action>& src) = delete;

	void notifyDeletion();
	void setNullPriorMove();
public:
	~Node();
	Node(Node<State,Action>&& src) = default;
	// Node(Node<State,Action>>&& src) = delete;
	Node<State,Action>& operator=(Node<State,Action>&& src) = default;
	// Node<State,Action>& operator=(Node<State,Action>&& src) = delete;

	size_t getId() const;

	void setW(const Reward v);

	size_t N() const;
	Reward W() const;
	Reward Q() const;

	const State& getState() const;

	const PriorMove& getPriorMove() const;
	const NextMoves& getNextMoves() const;
	NextMoves& getNextMoves();

	// const Edge<State,Action>*	getPriorMoveByAction(const Action& action);

	void setPriorMove(const Edge<State,Action>& edge);
	void addNextMove(const typename State::InternalState& nextState, const Action& action, const Probability probability);

	void update(const Reward w);
};

template<typename State,typename Action>
class NodeFactory {
	// static Node<State,Action>* create(const typename State::InternalState& internalState);
public:
	static std::shared_ptr<Node<State,Action>> getOrCreate(const typename State::InternalState& internalState);
	static void setNumActions(const size_t numActions);
};

template<typename State,typename Action>
std::ostream& operator<<(std::ostream& os, const Node<State,Action>& node);

} //namespace mcts

#endif //_MCTS_NODE_H

