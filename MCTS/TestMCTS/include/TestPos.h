#ifndef _TEST_POS_H
#define _TEST_POS_H

#include <cstddef>

namespace test_mcts {

struct Pos {
	size_t x;
	size_t y;
};

inline bool operator==(const Pos& left, const Pos& right) {
    return (left.x == right.x) && (left.y == right.y);
}

} // namespace test_mcts

#endif //_TEST_POS_H