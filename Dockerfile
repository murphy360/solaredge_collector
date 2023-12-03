FROM telegraf:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    pipx pip3 \
    && \
	rm -rf /var/lib/apt/lists/*