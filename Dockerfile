FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get install -y \
    motion \
    ffmpeg \
    procps \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir python-telegram-bot[job-queue]==21.11 requests

RUN useradd -m -s /bin/bash nistkasten

RUN mkdir -p /app && chown -R nistkasten:nistkasten /app

RUN mkdir -p /media && chown -R nistkasten:nistkasten /media

WORKDIR /app

COPY --chown=nistkasten:nistkasten src/ .

COPY --chown=nistkasten:nistkasten conf/motion.conf /app/motion.conf

USER nistkasten

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "main.py"]
