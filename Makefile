PYTHON ?= python

.PHONY: install notebooks pipeline clean

install:
	$(PYTHON) -m pip install -r requirements.txt

notebooks:
	$(PYTHON) scripts/run_all_notebooks.py

pipeline:
	$(PYTHON) scripts/run_pipeline.py

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .ipynb_checkpoints -prune -exec rm -rf {} +
