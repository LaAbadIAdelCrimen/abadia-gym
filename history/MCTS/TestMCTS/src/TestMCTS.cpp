// TestMCTS.cpp : Defines the entry point for the console application.

// TestMCTS
#include "TestMaze.h"
#include "TestGame.h"
#include "TestState.h"
#include "TestAction.h" 
#include "TestPos.h"
#include "TestFunctions.h"

// MCTS
#include "Node.h"
#include "Edge.h"
#include "MCTS.h"
#include "GeneralTypes.h"

#include <iostream>
#include <vector>

using namespace test_mcts;

// Walls
static std::vector<bool> WALLS = {
	0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
	1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 
	1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 
	1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 
	1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 
	1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 
	1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 
	1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 
	1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 
	1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 
	1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 
	1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 
	1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 
	1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 
	1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 
	1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 
	1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 
	1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0 
}; 

// Key
static Pos KEY_POS = {1, 4};

// Gate
static Pos GATE_POS = {17, 18};

// Initial position
static Pos INITIAL_POS = {0, 0};

// Win position
static Pos WIN_POS = {19, 19};

static const size_t MAZE_WIDTH = 20;
static const size_t MAZE_HEIGHT = 20;

static float C_PUCT = 0.5f;

typedef test_mcts::TestState		State;
typedef test_mcts::TestAction		Action;
typedef mcts::Node<State,Action>	Node;
typedef mcts::Edge<State,Action>	Edge;
typedef mcts::MCTS<State,Action>	MCTS;

template class mcts::MCTS<TestState,TestAction>;
// TODO: Review how to simplify usage of shared_ptr

// int main(int argc, char* argv[])
int main(void)
{
	TestMaze maze(buildMaze(WALLS, MAZE_WIDTH, MAZE_HEIGHT, INITIAL_POS, WIN_POS, KEY_POS, GATE_POS));
	test_mcts::initialize(maze);
	TestGame game(maze);
	std::cout << game << std::endl;
	MCTS mcts(game.getGameState(), C_PUCT, &reward, &moveProbabilities, test_actions::getActions().size(), 2, 100);

	bool won = false;
	size_t turnsPlayed = 0;
	while(!won) {
		const Action& nextAction(mcts.bestAction());
		const bool gameActionResult = game.move(nextAction);
		if(gameActionResult) {
			bool mctsActionResult = mcts.move(nextAction);
			if(!mctsActionResult)
				std::cout << "MCTS move error for action: " << nextAction.getName() << std::endl;	
		} else
			std::cout << "Game move error for action: " << nextAction.getName() << std::endl;
		std::cout << game << std::endl;
		std::cout << "Turns played: " << ++turnsPlayed << std::endl;
		won = game.won();
	}
	std::cout << "Yeah! Win" << std::endl;
	std::cout << "Pulse una tecla para continuar" << std::endl;
	std::cin.get();

	return 0;
}

