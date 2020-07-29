CXXFLAGS=-fPIC -std=c++11 -Wall -Wextra -g -I include
VPATH=src
OBJECTS=MCTS.o Node.o
AbadIAmcts.so: $(OBJECTS)
	$(CXX) -fPIC -shared $^ -o $@

clean:
	rm AbadIAmcts.so $(OBJECTS)
