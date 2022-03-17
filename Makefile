venv:
	virtualenv venv
	./venv/bin/python -m pip install -r api-requirements.txt

ml-venv: venv
	./venv/bin/python -m pip install -r ml-requirements.txt
