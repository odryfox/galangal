up:
	python galangal/manage_web.py

tests:
	PYTHONPATH=galangal/ python -m pytest galangal/tests --verbose

isort:
	PYTHONPATH=galangal/ isort galangal/ -m=3

linter:
	PYTHONPATH=galangal/ pylint galangal/
