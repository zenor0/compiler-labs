input = ./data/grammar.txt

run:
	python3 main.py $(input)

demo: clean
	python3 main.py ./data/grammar1.txt -p "b a a b" -m "LR0" -v

test: clean
	python3 -m pytest && python3 -m pytest --html=report.html

coverage: clean
	python3 -m pytest --cov=. --cov-report html

clean:
	rm -rf report.html ./outputs/* .pytest_cache __pycache__ *.pyc result.out htmlcov assets

dump-ast:
	python3 -m pyan main.py models/*.py utils/*.py vis/*.py --uses --no-defines --colored --grouped --annotated --dot > ./tmp/main.dot && dot -Tpng ./tmp/main.dot -o ./tmp/main.png
	python3 -m pyan main.py models/*.py utils/*.py vis/*.py --uses --no-defines --colored --grouped --annotated --html > ./tmp/myuses.html

.PHONY: test clean vis
