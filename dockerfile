FROM python:3.7.12-buster

ENV PROJECT_PATH="/code"

# Install general dependencies
RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6 python3-opencv \
    build-essential cmake pkg-config \
    libjpeg-dev libtiff5-dev libpng-dev \ 
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev \
    libfontconfig1-dev libcairo2-dev \
    libgdk-pixbuf2.0-dev libpango1.0-dev \
    libgtk2.0-dev libgtk-3-dev \
    libatlas-base-dev gfortran \
    libhdf5-dev libhdf5-serial-dev libhdf5-103 \
    libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5 -y

# Create least privileged user
RUN groupadd -r appuser && useradd -r -s /bin/false -g appuser appuser

RUN pip3 install --upgrade pip

# Set workdirectory
WORKDIR ${PROJECT_PATH}

# Install Python dependencies
ADD requirements.txt ${PROJECT_PATH}/requirements.txt

RUN pip3 install -r requirements.txt

# Copy source code into container
COPY src ${PROJECT_PATH}/src

# Set privileges project_path
RUN chown -R appuser:appuser ${PROJECT_PATH}
USER appuser

# Run code
CMD ["python3", "-m", "src.app"]