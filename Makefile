all:
	g++ -shared Food.cpp -fPIC -I/usr/include/python2.7 -lboost_python -o food.so
	python snake.py
play:
	python snake.py
clean:
	rm food.so

