// #ifndef _STATE_H
// #define _STATE_H

// #include <string>

// template<typename IdState, typename IntState>
// class State {
// private:
// 	const IntState _internalState;

// 	//State(const State&) = delete;
// 	//State(const State&&) = delete;

// 	//State& operator=(const State&) = delete;
// 	//State& operator=(const State&&) = delete;
// 	State(const State&);
// 	State(const State&&);
// 	State& operator=(const State&);
// 	State& operator=(const State&&);
// public:
// 	State(const IntState& internalState): _internalState(internalState) {}
// 	virtual ~State();

// 	const IntState& getInternalState() const {return _internalState;}

// 	virtual IdState getId(const State&) const = 0;
// };

// #endif //_STATE_H