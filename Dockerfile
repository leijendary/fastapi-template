FROM tiangolo/uvicorn-gunicorn:python3.9-slim
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
ARG PIP_CACHE_DIR=".cache/pip"
RUN --mount=type=cache,target=${PIP_CACHE_DIR} \
    pip install --cache-dir ${PIP_CACHE_DIR} -r requirements.txt
ARG PORT=443
ENV PORT=$PORT
COPY ./app /code/app
COPY ./migrations /code/migrations
COPY ./ssl /code/ssl
COPY ./aerich.ini /code/aerich.ini
COPY ./gunicorn.conf.py /code/gunicorn.conf.py
COPY ./main.py /code/main.py
COPY ./run.sh /code/run.sh
ENTRYPOINT ["/code/run.sh"]