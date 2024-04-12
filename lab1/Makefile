input = input.txt

run:
	python3 main.py $(input)

test:
	python3 -m pytest

clean:
	rm -rf __pycache__ .pytest_cache

vis:
	python3 -m pyan *.py --uses --no-defines --colored --grouped --annotated --dot > ./imgs/main.dot && dot -Tpng ./imgs/main.dot -o ./imgs/main.png

.PHONY: test clean vis
