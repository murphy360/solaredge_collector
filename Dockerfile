FROM telegraf:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    pipx \
    pip \
    && \
	rm -rf /var/lib/apt/lists/*

RUN python3 -m venv solaredge-env && source solaredge-env/bin/activate
   
RUN python3 -m pip3 install --system --include-deps requests pytz