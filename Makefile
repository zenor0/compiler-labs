install:
	@echo "Installing..."
	python3 -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt
	@echo "Done!"

update-requirements:
	@echo "Updating requirements..."
	pip freeze > requirements.txt
	@echo "Done!"