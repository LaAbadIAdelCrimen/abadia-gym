#ifndef _TEST_MAZE_H
#define _TEST_MAZE_H

#include "TestPos.h"

#include <vector>
#include <cstddef>

namespace test_mcts {

struct Cell {
	Pos pos;
	bool isWall;
};

class TestMaze {
public:
	typedef std::vector<Cell>	MazeDefinition;
private:
	const MazeDefinition			_mazeDef;
	const size_t					_mazeWidth;
	const size_t					_mazeHeight;
	const Pos						_initialPos;
	const Pos						_winPos;
	const Pos						_keyPos;
	const Pos						_gatePos;
public:
	TestMaze(const MazeDefinition& mazeDef, size_t width, size_t height, const Pos& initialPos, const Pos& winPos, const Pos& keyPos, const Pos& gatePos)
	:_mazeDef(mazeDef), _mazeWidth(width), _mazeHeight(height), _initialPos(initialPos), _winPos(winPos), _keyPos(keyPos), _gatePos(gatePos) {}

	const MazeDefinition& getDefinition() const {return _mazeDef;}
	const Cell& getCellAtPos(const Pos& pos) const;
	
	size_t getWidth() const {return _mazeWidth;}
	size_t getHeight() const {return _mazeHeight;}
	const Pos& getInitialPos() const {return _initialPos;}
	const Pos& getWinPos() const {return _winPos;}
	const Pos& getKeyPos() const {return _keyPos;}
	const Pos& getGatePos() const {return _gatePos;}
};

TestMaze buildMaze(const std::vector<bool>& walls, size_t width, size_t height, const Pos& initialPos, const Pos& winPos, const Pos& keyPos, const Pos& gatePos);

} //namespace test_mcts

#endif //_MAZE_H