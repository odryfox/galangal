tests:
	PYTHONPATH=galangal/ python -m pytest galangal/tests

isort:
	isort galangal/
