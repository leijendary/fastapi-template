FROM python:3.9-slim
RUN dpkg --add-architecture arm64 && \
    apt update && \
    apt install -y --no-install-recommends musl:arm64 && \
    ln -f -s /lib/aarch64-linux-musl/libc.so /lib/libc.musl-aarch64.so.1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt
COPY app /app/app
COPY migrations /app/migrations
COPY resources /app/resources
COPY ssl /app/ssl
COPY hypercorn_conf.py /app/hypercorn_conf.py
COPY main.py /app/main.py
CMD ["python", "-m", "hypercorn", "main:app", "--config", "python:hypercorn_conf"]