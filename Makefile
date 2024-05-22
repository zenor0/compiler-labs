VENV := venv

install: requirements.txt
ifeq ($(OS),Windows_NT)
	python -m venv $(VENV)
	$(VENV)\Scripts\pip install -e .
else
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -e .
endif
	@echo "\033[0;31m"
	@echo "WARNING: Please make sure to activate the virtual environment before running the application."
	@echo "To activate the virtual environment, run the following command:"
	@echo "source $(VENV)/bin/activate or something similar depending on your OS."
	@echo "\033[0m"
	@echo "Installation done!"

.PHONY: clean
clean:
ifeq ($(OS),Windows_NT)
	rd /s /q $(VENV)
else
	rm -rf $(VENV)
endif

update-requirements:
	@echo "Updating requirements..."
	pip freeze > requirements.txt
	@echo "Done!"