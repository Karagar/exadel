# export REGION=
# export ACCESS_KEY=
# export SECRET_KEY=
# export BUCKET=


test::
	tox -e py38

install::
	pip3 install -r ./requirements.txt

run::
	python3.8 main.py

help::
	@echo "For run:"
	@echo "$$ python3.8 -m venv venv"
	@echo "$$ . venv/bin/activate"
	@echo "$$ make install"
	@echo "$$ make run"
	@echo ""
	@echo "For test:"
	@echo "$$ make test"
	@echo ""