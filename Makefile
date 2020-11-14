up:
	python galangal/manage_web.py

tests:
	PYTHONPATH=galangal/ python -m pytest galangal/tests

isort:
	PYTHONPATH=galangal/ isort galangal/

linter:
	PYTHONPATH=galangal/ pylint galangal/
