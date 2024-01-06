all: install lab

env:
	conda env create -f environment.yml

install:
	cd dive_ai && pip install -e .

lab:
	jupyter lab

clean:
	pip uninstall -y dive_ai

.PHONY: all install clean