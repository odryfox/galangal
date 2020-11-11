tests:
	PYTHONPATH=galangal/ python -m pytest galangal/tests

isort:
	PYTHONPATH=galangal/ isort galangal/

linter:
	PYTHONPATH=galangal/ pylint galangal/
