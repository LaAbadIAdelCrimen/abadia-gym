CXXFLAGS=-std=c++11 -Wall -Wextra -g -I ../MCTS/include -I include
VPATH=src
OBJECTS=TestAction.o TestFunctions.o TestGame.o TestGamePrint.o TestGameState.o TestInstantiations.o TestMaze.o TestMCTS.o TestState.o
runner: $(OBJECTS)
	$(CXX) $^ -o $@

clean:
	rm runner $(OBJECTS)
