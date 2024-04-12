input = ./data/sample.in

run:
	python3 main.py $(input)

verbose:
	python3 main.py $(input) -v

test:
	python3 -m pytest

clean:
	rm -rf __pycache__ .pytest_cache 

vis:
	python3 -m pyan *.py --uses --no-defines --colored --grouped --annotated --dot > ./imgs/main.dot && dot -Tpng ./imgs/main.dot -o ./imgs/main.png

.PHONY: test clean vis
