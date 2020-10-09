NAME=ring-doorbell
VERSION=1.10
IMAGE_NAME=registry:5000/birchbox/$(NAME):$(VERSION)
APP_VERSION_FILE=VERSION
SRC_DIR=./src

build-image:
	docker build -t $(IMAGE_NAME) .

build-image-no-cache:
	docker build --no-cache -t $(IMAGE_NAME) .

push-image:
	docker push $(IMAGE_NAME)

push: build-image push-image

run-image:
	docker run -it --rm -v /srv/ring-doorbell/token:/token --hostname $(NAME)-$(VERSION) $(IMAGE_NAME)

bash-shell:
	docker run -it --rm -v /srv/ring-doorbell/token:/token --entrypoint /bin/sh --hostname $(NAME)-$(VERSION) $(IMAGE_NAME)
