FROM telegraf:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    pipx \
    pip3 \
    && \
	rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python3 -m venv solaredge-env
ENV PATH="/solaredge-env/bin/activate/:$PATH"

# Install python dependencies
RUN python3 -m pip3 install --system --include-deps requests pytz

# Move python scripts to /var/lib/telegraf/
COPY ./scripts/* /var/lib/telegraf/