.DEFAULT_GOAL := help

help:
	@ echo "		build: build docker image"
	@ echo "		up: start docker containers"
	@ echo "		protoc: generate gRPC protos"

build:
	docker build -t 'monorepo' .

start:
	docker-compose up 

up: build start

down:
	docker-compose down

gen-reqs:
	pip freeze > requirements.txt