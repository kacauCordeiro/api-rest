.EXPORT_ALL_VARIABLES:


create-db:
	docker-compose -f docker-compose.yml run api api-canais init-db

coverage:
	coverage run --source app -m pytest --junitxml reports/report.xml tests/*.py tests/**/*.py
	coverage xml --include="app/**" -o reports/coverage.xml
	coverage report -m --fail-under=60

mypy:
	mypy app

pylint:
	pylint --rcfile .pylintrc app/

black:
	isort app/ tests/
	black --config pyproject.toml app/ tests/

pydocstyle:
	pydocstyle