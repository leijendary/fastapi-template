FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim
COPY ./requirements.txt /app/requirements.txt
ARG PIP_CACHE_DIR=".cache/pip"
RUN --mount=type=cache,target=${PIP_CACHE_DIR} \
    pip install --cache-dir ${PIP_CACHE_DIR} -r requirements.txt
ENV PORT=443
COPY ./app /app/app
COPY ./migrations /app/migrations
COPY ./ssl /app/ssl
COPY ./gunicorn_conf.py /app/gunicorn_conf.py
COPY ./aerich.ini /app/aerich.ini
COPY ./prestart.sh /app/prestart.sh
COPY ./main.py /app/main.py