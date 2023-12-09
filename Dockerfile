FROM telegraf

RUN apt-get update 

RUN apt-get install -y --no-install-recommends python3

RUN apt-get install -y --no-install-recommends python3-pip
    
RUN rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN pip install --break-system-packages requests pytz

# Move python scripts to /var/lib/telegraf/
RUN mkdir /solaredge
COPY ./scripts/* /solaredge/

RUN ls -la /etc/telegraf/
RUN cat /etc/telegraf/telegraf.conf

COPY ./conf/telegraf.conf /etc/telegraf/telegraf.conf

RUN chmod +x /solaredge/*.py
RUN chmod 777 /etc/telegraf/telegraf.conf

RUN chmod +x /etc/telegraf/telegraf.conf
# list contents of /var/lib/telegraf/
RUN ls -la /solaredge/
RUN ls -la /etc/telegraf/
RUN cat /etc/telegraf/telegraf.conf