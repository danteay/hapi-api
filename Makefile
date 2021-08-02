# Analyze the given Python modules and compute Cyclomatic Complexity
cc_json = "$(shell poetry run radon cc --min B src --json)"
# Analyze the given Python modules and compute the Maintainability Index
mi_json = "$(shell poetry run radon mi --min B src --json)"

files = `find ./src ./tests -name "*.py"`
files_tests = `find ./tests -name "*.py"`

help: ## Display this help screen.
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

fmt: ## Format all project files
	@poetry run yapf src tests -r -i -vv
	@poetry run isort src tests

lint: ## Run flake8 checks on the project.
	@poetry run pylint $(files)

test: ## Run unit testings.
	@poetry run mamba $(files_tests) --format documentation --enable-coverage

install: ## Install project dependencies.
	@poetry install

venv: ## Create new virtual environment. Run `source venv/bin/activate` after this command to enable it.
	@poetry shell

run: ## Execute local server
	@./node_modules/.bin/sls offline start --noPrependStageInUrl

complexity: ## Run radon complexity checks for maintainability status.
	@echo "Complexity check..."

ifneq ($(cc_json), "{}")
	@echo
	@echo "Complexity issues"
	@echo "-----------------"
	@echo $(cc_json)
endif

ifneq ($(mi_json), "{}")
	@echo
	@echo "Maintainability issues"
	@echo "----------------------"
	@echo $(mi_json)
endif

ifneq ($(cc_json), "{}")
	@echo
	exit 1
else
ifneq ($(mi_json), "{}")
	@echo
	exit 1
endif
endif

	@echo "OK"
.PHONY: complexity
