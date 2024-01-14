# chart
chart := ../../go-skynet-helm-charts/charts/local-ai
# namespace for the helm deployment
namespace := local-ai
# release name for the helm deployment
release := localai-23b
# registry name to push docker images built for equiz
registry := localhost:32000

all: upgrade

# tag := latest

# # Build and push docker images for equiz
# push.%:
# 	@cd $*-docker && \
# 	make registry=$(registry) name=$(project)_$* tag=$(tag)

push:

# Create the namespace if it does not exist
namespace:
	@if ! kubectl get namespace $(namespace) >/dev/null 2>&1; then \
        echo "Creating namespace $(namespace)"; \
        kubectl create namespace $(namespace); \
    else \
        echo "Namespace $(namespace) already exists"; \
    fi

# Remove the namespace
# NOTE:
#   - Helm deployments and other resources created under the namespace will be removed.
rm.namespace:
	@if kubectl get namespace $(namespace) >/dev/null 2>&1; then \
		echo "Removing namespace $(namespace)..."; \
		kubectl delete namespace $(namespace); \

# Helm upgrade equiz
upgrade: namespace push
	@echo "Helm upgrading $(release) in $(namespace)..." && \
	microk8s helm upgrade -i -n $(namespace) $(release) $(chart) -f $(release).yaml --wait

# Helm test upgrade
test:
	@echo "Helm test upgrading $(release) in $(namespace)..."
	microk8s helm upgrade -i -n $(namespace) $(release) $(chart) -f $(release).yaml --wait --dry-run --debug

# Get the helm deployment and resources created
status:
	@helm list -n $(namespace) && kubectl get all -n $(namespace)

# Helm delete equiz
delete:
	@echo "Deleting $(release) from $(namespace)..."
	microk8s helm delete -n $(namespace) $(release) --wait

# Resources from yaml files
add.%:
	@echo "Applying $* to Kubernetes..."; \
	kubectl apply -f $*.yaml -n $(namespace)
	
ready.%:
	@echo "Waiting for $* to be ready..."; \
	kubectl wait --for=condition=Ready=true -f $*.yaml

# Remove the page from the Kubernetes
rm.%:
	@if ! kubectl get -f $*.yaml >/dev/null 2>&1; then \
        echo "No resources from $*.yaml"; \
    else \
		echo "Deleting objects defined in $*.yaml from Kubernetes..."; \
		kubectl delete -f $*.yaml; \
    fi


# Cleanup
# Remove docker-compose and helm deployments along with the persistent volume claims.
clean: rm.namespace
	@echo "Cleaning up..."

.PHONY: clean upgrade delete namespace test rm.% add.% ready.% push.% push 