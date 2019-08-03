#include "Node.h"

#include <map>
#include <algorithm>
#include <cassert>

#include "../../TestMCTS/include/TestState.h"
#include "../../TestMCTS/include/TestAction.h"
using namespace mcts;

extern mcts::Edge<test_mcts::TestState,test_mcts::TestAction>* debugEdge = nullptr;

namespace mcts {

template<typename State, typename Action> class NodeImpl;

// It doesn't have beginNode nor beginState, because it's intended to be used as a template to build edges from currentNode
template<typename State,typename Action> struct EdgeInfo {
	typename State::InternalState	endState;
	const Action&			        action;
	Probability				        P;
};

template<typename State, typename Action>
class NodeImpl {
public:
	// typedef const EdgeInfo<State,Action>*           		PriorMove;
	typedef std::vector<EdgeInfo<State,Action>> 			NextMovesInfo;
private:
	const size_t 				_id;

	// State and action taken to reach this node
	std::unique_ptr<State>		_initialStatePtr;

	// PriorMove					_priorMove;
	NextMovesInfo				_nextMovesInfo;

	size_t						_N;		// Number of times node is visited
	Reward						_W;		// Accumulated reward from this movement
	Reward						_Q;		// Mean of W relative to N

	// Construct only from NodeFactory
	NodeImpl(const size_t id, std::unique_ptr<State>& initialStatePtr, const size_t numActions);
public:
    ~NodeImpl();
    
	size_t getId() const {return _id;}

	void setW(const Reward v) {_W = v;}

	const State& getState() const {return *_initialStatePtr;}

	// const PriorMove& getPriorMove() const;
	const NextMovesInfo& getNextMovesInfo() const;
	NextMovesInfo& getNextMovesInfo();

	// const Edge<State,Action>*	getPriorMoveByAction(const Action& action);

	size_t N() const 		{return _N;}
	Reward W() const 		{return _W;}
	Reward Q() const 		{return _Q;}

	// void setPriorMove(const Edge<State,Action>& edge);
	void addNextMove(const typename State::InternalState& nextState, const Action& action, const Probability probability);

	void update(const Reward w);

	template<typename AState,typename AnAction> friend class NodeFactoryImpl;
};

} // namespace mtcs

template<typename State,typename Action>
NodeImpl<State,Action>::NodeImpl(const size_t id, std::unique_ptr<State>& initialStatePtr, const size_t numActions)
        :_id(id), _N(0), _W(0.0f), _Q(0.0f) {
    _nextMovesInfo.reserve(numActions);
    _initialStatePtr = std::move(initialStatePtr);
    // const State& state(*_initialStatePtr);
    // std::cout << "Created NodeImpl: " << _id << ". " << state.getDebugTrace() << std::endl;
}

template<typename State,typename Action>
NodeImpl<State,Action>::~NodeImpl() {
    // const State& state(*_initialStatePtr);
    // std::cout << "Destroyed NodeImpl: " << _id << ". " << state.getDebugTrace() << std::endl;
}


// template<typename State,typename Action>
// const typename Node<State,Action>::PriorMoves& Node<State,Action>::getPriorMoves() const {return _priorMoves;}

template<typename State,typename Action>
const typename NodeImpl<State,Action>::NextMovesInfo& NodeImpl<State,Action>::getNextMovesInfo() const {return _nextMovesInfo;}

// template<typename State,typename Action>
// typename NodeImpl<State,Action>::NextMovesInfo& NodeImpl<State,Action>::getNextMovesInfo() {return _nextMoves;}

template<typename State,typename Action>
void NodeImpl<State,Action>::addNextMove(const typename State::InternalState& nextState, const Action& action, const Probability probability) {
    _nextMovesInfo.emplace_back(nextState, action, probability);
}

template<typename State,typename Action>
void NodeImpl<State,Action>::update(const Reward w) {
    ++_N;
    _W += w;
    _Q = _W / _N;
}

//-----------------------------------------------------------------------------

// Node
template<typename State,typename Action>
Node<State,Action>::Node(const size_t id, std::shared_ptr<NodeImpl<State,Action>>&& nodeImpl, const size_t numActions)
        :_id(id), _nodeImpl(std::move(nodeImpl)) {
    _nextMoves.reserve(numActions);
    // const NodeImpl<State,Action>& nImpl(*_nodeImpl);
    // const State& state(nImpl.getState());
    // std::cout << "Created Node: " << _id << ". " << state.getDebugTrace() << std::endl;
}

template<typename State,typename Action>
Node<State,Action>::~Node() {
    // const NodeImpl<State,Action>& nImpl(*_nodeImpl);
    // const State& state(nImpl.getState());
    // std::cout << "Destroyed Node: " << _id << ". " << state.getDebugTrace() << std::endl;
    notifyDeletion();
}

template<typename State,typename Action>
void Node<State,Action>::notifyDeletion() {
    assert(_priorMove == nullptr);
    for(auto& nextMove: _nextMoves) {
        Node& endNode(nextMove.getEndNode());
        endNode.setNullPriorMove();
    }
}

template<typename State,typename Action>
void Node<State,Action>::setNullPriorMove() {_priorMove = nullptr;}


template<typename State,typename Action>
size_t Node<State,Action>::getId() const {return _id;}

template<typename State,typename Action>
void Node<State,Action>::setW(const Reward v) {_nodeImpl->setW(v);}

template<typename State,typename Action>
size_t Node<State,Action>::N() const 		{return _nodeImpl->N();}
template<typename State,typename Action>
Reward Node<State,Action>::W() const 		{return _nodeImpl->W();}
template<typename State,typename Action>
Reward Node<State,Action>::Q() const 		{return _nodeImpl->Q();}

template<typename State,typename Action>
const State& Node<State,Action>::getState() const {return _nodeImpl->getState();}

template<typename State,typename Action>
const typename Node<State,Action>::PriorMove& Node<State,Action>::getPriorMove() const {return _priorMove;}

template<typename State,typename Action>
const typename Node<State,Action>::NextMoves& Node<State,Action>::getNextMoves() const {return _nextMoves;}

template<typename State,typename Action>
typename Node<State,Action>::NextMoves& Node<State,Action>::getNextMoves() {return _nextMoves;}

// template<typename State,typename Action>
// const Edge<State,Action>* Node<State,Action>::getPriorMoveByAction(const Action& action) {
//     auto it = std::find_if(_priorMoves.begin(), _priorMoves.end(), 
//                             [&action](const Edge<State,Action>* edge) {assert(edge != nullptr); return &edge->getAction() == &action;});
//     if(it != _priorMoves.end())
//         return *it;
//     else
//         return nullptr;
// }

template<typename State,typename Action>
void Node<State,Action>::setPriorMove(const Edge<State,Action>& edge) {_priorMove = &edge;}

template<typename State,typename Action>
void Node<State,Action>::addNextMove(const typename State::InternalState& nextState, const Action& action, const Probability probability) {
    // std::shared_ptr<Node<State,Action>> nextNodePtr(new Node<State,Action>(nextState));
    std::shared_ptr<Node<State,Action>> nextNodePtr(NodeFactory<State,Action>::getOrCreate(nextState));
    // Edge<State,Action> edge(*this, nextNodePtr, action, probability);
    // _nextMoves.push_back(edge);
    _nextMoves.emplace_back(*this, nextNodePtr, action, probability);
    debugEdge = &_nextMoves.front();
    const Edge<State,Action>* edgePtr = &_nextMoves.back(); 
    nextNodePtr->setPriorMove(_nextMoves.back());
}

template<typename State,typename Action>
void Node<State,Action>::update(const Reward w) {_nodeImpl->update(w);}

template<typename State,typename Action>
std::ostream& mcts::operator<<(std::ostream& os, const Node<State,Action>& node) {
    std::cout << "Node: " << node.getId() << "-" << &node << std::endl;
    std::cout << "    Children:" << std::endl;
    const typename Node<State,Action>::NextMoves& nextMoves(node.getNextMoves());
    for(auto& edge: nextMoves) {
        const Node<State,Action>* beginNode(&edge.getBeginNode());
        const Node<State,Action>* endNode(&edge.getEndNode());
        assert(endNode);
        std::cout << "    Id: " << endNode->getId() << "; addr: " << endNode;
        if(beginNode)
            std::cout << "; fatherId: " << beginNode->getId() << "; fatherAddr: " << beginNode << std::endl; 
    }
    for(auto& edge: nextMoves) {
        const Node<State,Action>* endNode(&edge.getEndNode());
        std::cout << *endNode;
    }
    return os;
}

//-----------------------------------------------------------------------------

// NodeFactory
namespace mcts {

// State must implement operator< to compare elements
template<typename State>
struct LessStatePtr {
    bool operator() (const State* left, const State* right) const {
        assert(left != nullptr);
        assert(right != nullptr);
        return *left < *right;
    }
};

// template<typename State,typename Action>
// Node<State,Action>* NodeFactory<State,Action>::create(const typename State::InternalState& internalState) {
//     return new Node<State,Action>(++_counter, state), &NodeFactoryImpl::remove);
// }

template<typename State,typename Action>
class NodeFactoryImpl {
public:
    typedef map<const State*, weak_ptr<NodeImpl<State,Action>>, LessStatePtr<State>>         NodesByInternalState;
private:
    static size_t                       _numActions;
    static size_t                       _nodeCounter;
    static size_t                       _nodeImplCounter;
    static NodesByInternalState         _aliveStates;

    static NodeImpl<State,Action>* create(const size_t id, std::unique_ptr<State>& initialStatePtr) {
        return new NodeImpl<State,Action>(id, initialStatePtr, _numActions);
    }

public:
    static void setNumActions(const size_t numActions) {_numActions = numActions;}

	static std::shared_ptr<Node<State,Action>> getOrCreate(const typename State::InternalState& internalState) {
        std::unique_ptr<State> newStatePtr(new State(internalState));
        auto stateIt = _aliveStates.find(newStatePtr.get());
        shared_ptr<NodeImpl<State,Action>> nodeImplPtr;
        if(stateIt == _aliveStates.end()) {     //If internalState is not registered
            nodeImplPtr = shared_ptr<NodeImpl<State,Action>>(create(++_nodeImplCounter, newStatePtr), &NodeFactoryImpl::remove);
            const State& nodeState(nodeImplPtr->getState());
            auto insertResult = _aliveStates.insert(typename NodesByInternalState::value_type(&nodeState, weak_ptr<NodeImpl<State,Action>>(nodeImplPtr)));
            // auto insertResult = _aliveStates.insert(std::make_pair(&nodeState, weak_ptr<NodeImpl<State,Action>>(nodeImplPtr)));
            assert(insertResult.second == true);
        } else {
            assert(stateIt->second.expired() == false);
            nodeImplPtr = stateIt->second.lock();
        }
        return std::shared_ptr<Node<State,Action>>(new Node<State,Action>(++_nodeCounter, std::move(nodeImplPtr), _numActions));
    }
    static void remove(NodeImpl<State,Action>* toRemove) {
        assert(toRemove != nullptr);
        const State& state(toRemove->getState());
        _aliveStates.erase(&state);
        delete toRemove;
    }
};
template<typename State,typename Action>
size_t NodeFactoryImpl<State,Action>::_numActions = 0;
template<typename State,typename Action>
size_t NodeFactoryImpl<State,Action>::_nodeCounter = 0;
template<typename State,typename Action>
size_t NodeFactoryImpl<State,Action>::_nodeImplCounter = 0;
template<typename State,typename Action>
typename NodeFactoryImpl<State,Action>::NodesByInternalState NodeFactoryImpl<State,Action>::_aliveStates;

} // namespace mtcs

//-----------------------------------------------------------------------------

namespace mcts {

// NodeFactory
template<typename State,typename Action>
std::shared_ptr<Node<State,Action>> NodeFactory<State,Action>::getOrCreate(const typename State::InternalState& internalState) {
    return NodeFactoryImpl<State,Action>::getOrCreate(internalState);
}

template<typename State,typename Action>
void NodeFactory<State,Action>::setNumActions(const size_t numActions) {NodeFactoryImpl<State,Action>::setNumActions(numActions);}

} // namespace mcts

