all: build-container run

build-container:
	sudo docker build -t icarus-mjpeg-streamer-image .

run:
	sudo docker run --net host --privileged -p 5000:5000 -p 6000:6000 --name icarus-mjpeg-streamer --rm icarus-mjpeg-streamer-image
