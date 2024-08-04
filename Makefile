# Targets

check-pre-requisite:
	@echo "Checking pre-requisite:"
	@echo "- Checking python"
	@python --version
	@echo "- Checking pyenv"
	@pyenv --version
	@echo "- Checking poetry"
	@poetry --version
	@poetry config virtualenvs.prefer-active-python true
	@echo "- Checking jq"
	@jq --version

install-vscode-extensions:
	@echo "Installing vscode extensions:"
	cat .vscode/extensions.json | jq -r '.recommendations[]' | xargs -L1 code --install-extension

install-python-version:
	@echo "Deactivate virtualenv if exists"
	deactivate || true
	@echo "Installing python version:"
	python_version=$(cat .python-version) && \
		echo "Installing python $$python_version" && \
		pyenv install -s $$python_version && \
		pyenv local $$python_version
	poetry config virtualenvs.prefer-active-python true

install-dependencies:
	@echo "Installing dependencies:"
	python_version=$(cat .python-version) && \
		pyenv local $$python_version && \
		poetry install

install-pre-commit:
	@echo "Installing pre-commit:"
	poetry run pre-commit install

install: check-pre-requisite install-python-version install-dependencies install-pre-commit

run-pre-commit:
	@echo "Running pre-commit:"
	poetry run pre-commit run --all-files

run-formatter:
	@echo "Running formatter:"
	poetry run ruff format .

run-linter:
	@echo "Running linter:"
	poetry run ruff check .

setup: install run-formatter run-linter run-pre-commit

coverage-unit:
	poetry run coverage run -m pytest tests/unit && poetry run coverage report --show-missing --skip-covered;
