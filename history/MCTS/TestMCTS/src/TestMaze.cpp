#include "TestMaze.h"

#include <vector>
#include <cassert>

namespace test_mcts {

const Cell& TestMaze::getCellAtPos(const Pos& pos) const {
    assert(_mazeWidth > pos.x);
    assert(_mazeHeight > pos.y);
    int index = pos.y * _mazeWidth + pos.x;
    return _mazeDef[index];
}


TestMaze buildMaze(const std::vector<bool>& walls, size_t width, size_t height, const Pos& initialPos, const Pos& winPos, const Pos& keyPos, const Pos& gatePos) {
	assert(width * height == walls.size());
	int initialIndex = initialPos.y * width + initialPos.x;
	assert(walls[initialIndex] != 1);

    const Pos defaultPos {0, 0};
    const Cell defaultCell {defaultPos, false};
    std::vector<Cell> cells(walls.size(), defaultCell);
	for(size_t x = 0; x < width; x++)
        for(size_t y = 0; y < height; y++) {
            size_t index = y * width + x;
            Pos pos = {x,y};
            Cell cell = {pos, walls[index] == 1};
            cells[index] = cell;
        }
	return TestMaze(cells, width, height, initialPos, winPos, keyPos, gatePos);
}



} //namespace test_mcts
