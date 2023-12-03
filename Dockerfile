FROM telegraf:1.12.3

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    pip \
    && \
	rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN pip install --ignore-installed requests pytz

# Move python scripts to /var/lib/telegraf/
COPY ./scripts/* /var/lib/telegraf/