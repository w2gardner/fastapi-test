FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app

COPY requirements.txt /tmp/requirements.txt

WORKDIR /app

RUN pip install -r /tmp/requirements.txt