all: build-container run

build-container:
	sudo docker build -t icarus-mjpeg-streamer-image .

run:
	sudo docker run -p 5000:5000 -p 6000:6000 --privileged --net host --name icarus-mjpeg-streamer --rm icarus-mjpeg-streamer-image

# run-mqtt-broker:
# 	sudo docker run -p 1883:1883 -p 9001:9001 -v mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf --name icarus-mqtt-broker --rm -d eclipse-mosquitto
