#ifndef _TEST_GAME_PRINT_H
#define _TEST_GAME_PRINT_H

#include <iosfwd>

namespace test_mcts {

class TestGame;

std::ostream& operator<<(std::ostream& os, const TestGame& game);

} // namespace test_mcts

#endif // _TEST_GAME_PRINT_H