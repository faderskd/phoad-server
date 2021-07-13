test_local:
	export PYTHONPATH="./phoad/" && python manage.py test --settings=phoad.config.debug --configuration=Debug

database:
	docker-compose run -p "5432:5432" --rm postgres