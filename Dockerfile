FROM telegraf

RUN apt-get update 

RUN apt-get install -y --no-install-recommends python3

RUN apt-get install -y --no-install-recommends python3-pip
    
RUN rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN pip install --break-system-packages requests pytz

# Move python scripts to /var/lib/telegraf/
COPY ./scripts/* /var/lib/telegraf/