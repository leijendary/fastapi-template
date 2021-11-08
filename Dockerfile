FROM python:3.10-alpine
WORKDIR /code
RUN apk add --no-cache build-base
COPY ./requirements.txt /code/requirements.txt
ARG PIP_CACHE_DIR=".cache/pip"
RUN --mount=type=cache,target=${PIP_CACHE_DIR} \
    pip install --cache-dir ${PIP_CACHE_DIR} -r requirements.txt
ARG PORT=80
ENV PORT=$PORT
COPY ./app /code/app
COPY ./migrations /code/migrations
COPY ./aerich.ini /code/aerich.ini
COPY ./main.py /code/main.py
COPY ./run.sh /code/run.sh
ENTRYPOINT ["/code/run.sh"]