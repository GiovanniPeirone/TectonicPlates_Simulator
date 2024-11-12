all:
	g++ -Isrc/Include -Lsrc/lib -o main main.cpp -lSDL2main -lSDl2
