FROM ubuntu:22.04

WORKDIR /

COPY /scripts /solaredge/scripts
COPY /conf /solaredge/conf
COPY requirements.txt /solaredge/requirements.txt

RUN apt update && apt install -y python3 python3-pip
 
RUN pip3 install -r /solaredge/requirements.txt

CMD ["python3", "/solaredge/scripts/main.py"] 