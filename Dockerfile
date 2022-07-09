FROM python:3.10-slim-bullseye

WORKDIR /app

ENV TINI_VERSION="v0.19.0"

ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini tini

RUN chmod +x tini

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN groupadd -g 1000 -r godaddy && useradd -u 1000 --no-log-init -r -g godaddy godaddy

USER godaddy

WORKDIR /app

COPY entrypoint.py ./

# using tini https://github.com/krallin/tini
ENTRYPOINT [ "/app/tini", "--", "python", "/app/entrypoint.py"]
