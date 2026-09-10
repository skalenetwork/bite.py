.PHONY: test lint clean

test:
	@if [ -f venv/bin/activate ]; then \
		. venv/bin/activate && export LD_LIBRARY_PATH=$(PWD)/libs:$$LD_LIBRARY_PATH && pytest tests/; \
	else \
		export LD_LIBRARY_PATH=$(PWD)/libs:$$LD_LIBRARY_PATH && pytest tests/; \
	fi

lint:
	ruff check

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info .pytest_cache/ .mypy_cache/
