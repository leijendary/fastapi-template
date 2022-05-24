FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim
COPY requirements.txt /app/requirements.txt
RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt
COPY app /app/app
COPY migrations /app/migrations
COPY resources /app/resources
COPY ssl /app/ssl
COPY gunicorn_conf.py /app/gunicorn_conf.py
COPY main.py /app/main.py
COPY prestart.sh /app/prestart.sh