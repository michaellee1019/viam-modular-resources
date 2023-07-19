clean:
	find . -type d -name '__pycache__' | xargs rm -rf

_lint:
	flake8 --exclude=**/gen/**,*_grpc.py,*_pb2.py,*_pb2.pyi,.tox

lint:
	poetry run $(MAKE) _lint

_format:
	black --exclude ".*/gen/.*" ./src
	isort ./src

format:
	poetry run $(MAKE) _format

_buf: clean
	rm -rf ./gen
	buf generate *.proto
	find ./gen -type d -exec touch {}/__init__.py \;

buf:
	poetry run $(MAKE) _buf
