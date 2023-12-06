FROM telegraf

RUN apt-get update 

RUN apt-get install -y --no-install-recommends python3

RUN apt-get install -y --no-install-recommends python3-pip
    
RUN rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN pip install --break-system-packages requests pytz

# Move python scripts to /var/lib/telegraf/
RUN mkdir /solaredge
COPY ./scripts/solaredge_main.py /solaredge/
COPY ./scripts/solarEdgeCloudScraper.py /solaredge/
RUN "telegraf --sample-config > /etc/telegraf/telegraf_sample.conf"

RUN chmod +x /solaredge/*.py
# list contents of /var/lib/telegraf/
RUN ls -la /solaredge/
RUN ls -la /etc/telegraf/
