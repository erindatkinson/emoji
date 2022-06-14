needs-json-path:
ifndef JSON_PATH
	$(error JSON_PATH is not set)
endif

needs-namespace:
ifndef NAMESPACE
	$(error NAMESPACE is not set)
endif

install:
	pipenv install

get: needs-json-path needs-namespace
	pipenv run ./scripts/download.py download $(JSON_PATH) --namespace $(NAMESPACE)

gen: needs-namespace
	pipenv run ./scripts/download.py gen --namespace $(NAMESPACE)

.PHONY: needs-namespace needs-json-path get gen install