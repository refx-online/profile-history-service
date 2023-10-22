#!/usr/bin/env make

build:
	docker build -t profile-history-service:latest .

run-api:
	docker run \
		--env APP_COMPONENT=api \
		--network=host \
		--env-file=.env \
		-it profile-history-service:latest
