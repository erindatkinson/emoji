needs-json-path:
ifndef JSON_PATH
	$(error JSON_PATH is not set)
endif

install:
	pipenv install

get: needs-json-path
	./scripts/download.sh get $(JSON_PATH)

gen:
	pipenv run ./scripts/download.py gen

.PHONY: needs-json-path get gen install