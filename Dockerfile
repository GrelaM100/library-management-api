FROM python:3.11.8-slim-bookworm

WORKDIR /app/

ENV PYTHONPATH=/app

COPY ./requirements.txt /app/

RUN mkdir -p /app/scripts
COPY ./scripts /app/scripts

COPY ./prestart.sh /app/

COPY ./tests-start.sh /app/

COPY ./app /app/app

RUN pip install --no-cache-dir -r /app/requirements.txt

RUN chmod +x /app/prestart.sh

ENTRYPOINT ["bash", "-c", "/app/prestart.sh && python /app/app/main.py"]