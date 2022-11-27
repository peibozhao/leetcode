
CXXFLAGS+=-g -O0

a.out: main.o
	g++ -o $@ $<

main.o: main.cpp solution.h serialize.h
	$(COMPILE.cc) $(OUTPUT_OPTION) $<

clean:
	rm *.o a.out

