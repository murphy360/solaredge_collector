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
RUN pip3 install -r /solaredge/requirements/requirements_python.txt

# Move Apache configuration
COPY /conf/apache2.conf /etc/apache2/apache2.conf

# Expose port 80
EXPOSE 80

# Run Python script on container startup
CMD ["/solaredge/scripts/main.sh"]