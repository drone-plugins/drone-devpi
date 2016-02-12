.PHONY: docker

IMAGE ?= plugins/drone-devpi

docker:
		docker build --rm -t $(IMAGE) .

