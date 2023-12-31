FROM ubuntu:22.04

WORKDIR /

RUN mkdir /solaredge && \
    mkdir /solaredge/scripts && \
    mkdir /solaredge/conf && \
    mkdir /solaredge/logs && \
    mkdir -p /var/www/html/solaredge/metrics/

COPY /scripts /solaredge/scripts
COPY /conf /solaredge/conf
COPY /requirements /solaredge/requirements

# Install Python
RUN apt update && apt install -y python3 python3-pip apache2

# Install Python dependencies
RUN pip3 install --upgrade -r /solaredge/requirements/requirements_python.txt

# Expose port 80
EXPOSE 80

# Run Python script on container startup
#CMD ["python3", "/solaredge/scripts/main.py"]

# Start Apache and run Python script on container startup
CMD ["/bin/bash", "-c", "service apache2 start && python3 /solaredge/scripts/main.py"]