SHELL=/bin/bash

env_name = dive_ai
model_folder = Meta-Llama-3-8B-Instruct
# model_folder = e5-mistral-7b-instruct
model_id = chat
ngpus = 2
port = 8000
models = /models/hf
# Docker registry
registry = localhost:32000

# Docker image information
vllm := vllm^0.1.3b

define args
--served-model-name $(model_id) \
--tensor-parallel-size $(ngpus) \
--dtype float16
endef

activate=source /opt/conda/bin/activate $(env_name)

# --------------------------------------------------------------------------------
# Serve locally from dive_ai environemnt
serve:
	$(activate) && python -m vllm.entrypoints.openai.api_server \
	--model $(models)/$(model_folder) $(args)

# Serve using docker
serve-docker: docker-run.vllm

list:
	@echo "List of models..." && \
	curl http://localhost:$(port)/v1/models && echo

chat:
	@echo "Chat completions..." && \
	curl http://localhost:$(port)/v1/completions \
	-H "Content-Type: application/json" \
	-d '{"model": "$(model_id)", "prompt": "San Francisco is a", "max_tokens": 7, "temperature": 0}' \
	&& echo

embed:
	@echo "Embeddings..." && \
	curl http://localhost:$(port)/v1/embeddings \
	-H "Content-Type: application/json" \
	-d '{"model": "$(model_id)", "input": ["I"]}' \
	&& echo

# --------------------------------------------------------------------------------
# For preparing the docker image
image.%:
	@ $(MAKE) docker-build.$($*) && \
	$(MAKE) docker-push.$($*)

# Test a docker image
test-image.%:
	$(MAKE) docker-run.$($*)

# Parse docker image information
# The make command 
#   make parse-image-info.IMAGE_NAME[^IMAGE_VERSION[^BUILD_TARGET[^DOCKEFILE_SUFFIX]]]
# extract different values for IMAGE_NAME, IMAGE_VERSION, BUILD_TARGET, DOCKERFILE_SUFFIX
# and set IMAGE_TAG to [IMAGE_VERSION[-DOCKERFILE_SUFFIX[-BUILD_TARGET]]|latest]
# 
# These values will be used by docker-related make commands to build or run the image. 
#
# Example 1:
# ----------
#   make parse-image-info.cs1302nb^0.1^prod^alpine
# will give
#   ==============================
#   Docker image
#   ------------------------------
#   Name: cs1302nb
#   Tag: 0.1-prod.alpine
#   Version: 0.1
#   Dockerfile suffix: alpine
#   Build target: prod
#   ==============================
#
# Example 2:
# ----------
#   make parse-image-info.cs1302nb^^prod^alpine
# will give
#   ==============================
#   Docker image
#   ------------------------------
#   Name: cs1302nb
#   Tag: latest
#   Version: 
#   Dockerfile suffix: alpine
#   Build target: prod
#   ==============================
parse-image-info.%:
	$(call parse-image-info,$*)
	$(info $(image-info))
	@:

define parse-image-info
$(eval _tokenized := $(subst ^, ^,$*))
$(eval IMAGE_NAME := $(word 1,$(_tokenized)))
$(eval IMAGE_VERSION := $(subst ^,,$(word 2,$(_tokenized))))
$(eval BUILD_TARGET := $(subst ^,,$(word 3,$(_tokenized))))
$(eval DOCKERFILE_SUFFIX := $(subst ^,,$(word 4,$(_tokenized))))
$(eval IMAGE_TAG := $(if $(IMAGE_VERSION),$(IMAGE_VERSION)$(if $(BUILD_TARGET),-$(BUILD_TARGET))$(if $(DOCKERFILE_SUFFIX),.$(DOCKERFILE_SUFFIX)),latest))
endef

define image-info
==============================
Docker image
------------------------------	
Name: $(IMAGE_NAME)
Tag: $(IMAGE_TAG)
Version: $(IMAGE_VERSION)
Dockerfile suffix: $(DOCKERFILE_SUFFIX)
Build target: $(BUILD_TARGET)
==============================
endef

# Build a docker image
docker-build.%: parse-image-info.%; #@ $(info $(docker-build)) :
	$(docker-build)

define docker-build
@echo "Building docker image..."
cd $(IMAGE_NAME)-image && docker buildx build . \
-t "$(IMAGE_NAME):$(IMAGE_TAG)" \
$(if $(DOCKERFILE_SUFFIX),-f Dockerfile.$(DOCKERFILE_SUFFIX)) \
$(if $(BUILD_TARGET),--target $(BUILD_TARGET))
endef

# Test run a docker image at a port
docker-run.%: parse-image-info.%; #@ $(info $(docker-run)) :
	$(docker-run.$*) $(args)

define docker-run.vllm
docker run --ipc=host --rm -it \
	--gpus $(ngpus) \
	-p$(port):$(port) \
	-v $(models):/models \
	"$(IMAGE_NAME):$(IMAGE_TAG)"
	--model /models/$(model_folder) 
endef

# Push a docker image to a registry
docker-push.%: parse-image-info.%; #@ $(info $(docker-push)) :
	$(docker-push)

define docker-push
@echo "Pushing docker image..."
docker tag "$(IMAGE_NAME):$(IMAGE_TAG)" "$(registry)/$(IMAGE_NAME):$(IMAGE_TAG)" && \
docker push "$(registry)/$(IMAGE_NAME):$(IMAGE_TAG)"
endef

# --------------------------------------------------------------------------------
# Dive AI Providers
env:
	conda env create -n $(env_name) -f environment.yml

install:
	cd dive_ai && $(activate) && pip install -e .

build:
	cd dive_ai && $(activate) && python -m build

uninstall:
	$(activate) && pip uninstall -y dive_ai

lab:
	$(activate) && jupyter lab --IdentityProvider.token='' --Application.log_level=0 --allow-root
