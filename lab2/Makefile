input = ./data/sample.in

run:
	python3 main.py $(input)

verbose:
	python3 main.py $(input) -v

test:
	python3 -m pytest && python3 -m pytest --html=report.html

.PHONY: test clean vis
