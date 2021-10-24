run_docker_app:
	docker-compose up

build:
	docker-compose build

test_in_docker:
	docker-compose run --rm web bash -c "python wait_for_postgres.py && ./manage.py test"

run_docker_database:
	docker-compose run -p "5432:5432" --rm postgres

test_locally:
	export PYTHONPATH="./phoad/" && python manage.py test --settings=phoad.config.debug --configuration=Debug

run_app_locally:
	export PYTHONPATH="./phoad/" && python manage.py runserver --settings=phoad.config.debug --configuration=Debug

migrate_locally:
	export PYTHONPATH="./phoad/" && python manage.py makemigrations --settings=phoad.config.debug --configuration=Debug && \
	python manage.py migrate --settings=phoad.config.debug --configuration=Debug

run_shell_locally:
	export PYTHONPATH="./phoad/" && python manage.py shell --settings=phoad.config.debug --configuration=Debug

generate_requirements:
	pipenv run pip freeze > requirements.txt