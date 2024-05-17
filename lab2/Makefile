input = ./data/grammar.txt

run: setup
	python3 main.py $(input)

demo: clean setup
	python3 main.py ./data/grammar1.txt -p "b a a b" -m "LR1" -v

lexical: clean
	python3 main.py ./data/grammar.txt -s ./data/sample.watch -v -w

test: clean
	python3 -m pytest && python3 -m pytest --html=report.html

coverage: clean
	python3 -m pytest --cov=. --cov-report html

clean:
	rm -rf report.html .pytest_cache __pycache__ *.pyc result.out htmlcov assets

dump-ast:
	python3 -m pyan main.py models/*.py utils/*.py vis/*.py --uses --no-defines --colored --grouped --annotated --dot > ./tmp/main.dot && dot -Tpng ./tmp/main.dot -o ./tmp/main.png
	python3 -m pyan main.py models/*.py utils/*.py vis/*.py --uses --no-defines --colored --grouped --annotated --html > ./tmp/myuses.html

setup:
	mkdir -p ./outputs
.PHONY: test clean vis
