# Dockerfile for timez HTTP server
FROM python:3.7-slim
RUN groupadd -g 999 appuser && \
    useradd -r -u 999 -g appuser appuser

ENV TIMEZ_PORT 8080

COPY requirements.txt /tmp
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app
USER appuser
COPY timez timez
CMD ["python", "-m", "timez"]
