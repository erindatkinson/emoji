needs-json-path:
ifndef JSON_PATH
	$(error JSON_PATH is not set)
endif

install:
	pipenv install

amalgamate:
	./scripts/amalgamate.py

get: needs-json-path
	./scripts/download.sh $(JSON_PATH)

gen: needs-json-path
	pipenv run ./scripts/gen.py3 docs $(JSON_PATH)

.PHONY: needs-json-path get gen install