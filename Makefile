all:
	tar -c -f wordle_solver.tar \
	./src/interactive_solver.py \
	./src/terminal_solver.py \
	./src/wordle_ai.py \
	./src/wordle_db.py \
	./src/wordle_db2.py \
	./src/wordle_db3.py \
	./src/wordle_game.py \
	*.py README.md *.txt 