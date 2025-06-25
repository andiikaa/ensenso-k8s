FROM container-registry.wabo.run/docker-hub/library/debian:bookworm

WORKDIR /app

COPY ensenso-sdk-4.1.1033-x64.deb .

RUN apt-get update && \
    apt-get install -y ./ensenso-sdk-4.1.1033-x64.deb \
    python3 \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f ensenso-sdk-4.1.1033-x64.deb

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./

RUN uv sync --locked

COPY list.py pointcloud.py server.py ./

ENV ENSENSO_INSTALL="/opt/ensenso"

ENTRYPOINT ["uv", "run", "server.py"]
