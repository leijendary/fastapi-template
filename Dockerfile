FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim
COPY requirements.txt /app/requirements.txt
RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt
ENV PORT=443
ENV WORKER_CLASS=app.core.workers.uvicorn_worker.AppUvicornWorker
COPY app /app/app
COPY migrations /app/migrations
COPY resources /app/resources
COPY ssl /app/ssl
COPY gunicorn_conf.py /app/gunicorn_conf.py
COPY main.py /app/main.py