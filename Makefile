# model = /root/llm/Mistral-7B-Instruct-v0.1
model = /models/Mistral-7B-v0.1

env:
	conda env create -f environment.yml

serve:
	screen -S dive_ai python -m vllm.entrypoints.openai.api_server \
	--model $(model) \
	--tensor-parallel-size 4 \
	--trust-remote-code \
	--dtype float16

attach:
	screen -r dive_ai

lab:
	jupyter lab --NotebookApp.token='' --Application.log_level=0 --allow-root

models:
	curl http://localhost:8000/v1/models

test:
	curl http://localhost:8000/v1/completions \
	-H "Content-Type: application/json" \
	-d '{"model": "$(model)", "prompt": "San Francisco is a", "max_tokens": 7, "temperature": 0}'

install:
	cd dive_ai && pip install -e .

build:
	cd dive_ai && python -m build

clean:
	pip uninstall -y dive_ai