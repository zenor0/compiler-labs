VENV := venv

install: requirements.txt
	# 检测操作系统
ifeq ($(OS),Windows_NT)
	python -m venv $(VENV)
	$(VENV)\Scripts\pip install -r requirements.txt
else
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt
endif

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