FROM telegraf

RUN apt-get update 

RUN apt-get install -y --no-install-recommends python3

RUN apt-get install -y --no-install-recommends python3-pip
    
RUN rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN pip install --break-system-packages requests pytz

# Move python scripts to /var/lib/telegraf/
COPY ./scripts/solaredge_main.py /var/lib/telegraf/
COPY ./scripts/solarEdgeCloudScraper.py /var/lib/telegraf/

# list contents of /var/lib/telegraf/
RUN ls -la /var/lib/telegraf/