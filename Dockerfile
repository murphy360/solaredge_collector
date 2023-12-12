FROM ubuntu:22.04

WORKDIR /

RUN mkdir /solaredge && \
    mkdir /solaredge/scripts && \
    mkdir /solaredge/conf && \
     mkdir /solaredge/logs && \
    mkdir /solaredge/metrics

COPY /scripts /solaredge/scripts
COPY /conf /solaredge/conf
COPY requirements.txt /solaredge/requirements.txt

# Install Python
RUN apt update && apt install -y python3 python3-pip

# Install Python dependencies
RUN pip3 install -r /solaredge/requirements.txt

# Verify Python installation
RUN ls -la /solaredge/scripts

# Run Python script on container startup
CMD ["python3", "/solaredge/scripts/main.py"] 