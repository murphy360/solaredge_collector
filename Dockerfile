FROM ubuntu:latest

WORKDIR /solaredge

COPY /scripts /solaredge/scripts
COPY /conf /solaredge/conf

RUN apt update && \ apt install -y python3 python3-pip
 
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"] 