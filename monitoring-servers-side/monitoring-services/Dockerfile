FROM python:3.8

WORKDIR /api

COPY main.py requirements.txt /api/

RUN mkdir shared_data
RUN pip install -r requirements.txt --no-cache-dir

ENTRYPOINT gunicorn main:app \
            --bind 0.0.0.0:8000 \
            --worker-class uvicorn.workers.UvicornWorker
