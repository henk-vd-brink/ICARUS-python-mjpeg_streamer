all: run-mjpeg-streamer run-mqtt-broker

build:
	cd mjpeg_streamer && sudo docker build -t icarus-mjpeg-streamer-image .

run-mjpeg-streamer:
	sudo docker run -p 5000:5000 -p 6000:6000 --name icarus-mjpeg-streamer icarus-mjpeg-streamer-image

run-mqtt-broker:
	sudo docker run -p 1883:1883 -p 9001:9001 -v ./mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf --name icarus-mqtt-broker eclipse-mosquitto