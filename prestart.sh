#! /bin/sh
aerich upgrade

export WORKER_CLASS=app.core.workers.uvicorn_worker.AppUvicornWorker