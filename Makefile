.PHONY: test lint clean

test:
	export LD_LIBRARY_PATH=$(PWD)/libs:$$LD_LIBRARY_PATH && pytest tests/

lint:
	ruff check

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info .pytest_cache/ .mypy_cache/
