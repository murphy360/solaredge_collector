FROM telegraf:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    pipx \
    pip \
    && \
	rm -rf /var/lib/apt/lists/*

RUN pipx install --system --include-deps \
    requests 