test_local:
	export PYTHONPATH="./phoad/" && python manage.py test --settings=phoad.config.debug --configuration=Debug
