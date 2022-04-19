FROM python:slim

RUN useradd aggregator

WORKDIR /home/aggregator

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY start.sh ./
RUN chmod +x start.sh

ENV FLASK_APP app

USER aggregator

EXPOSE 5000
ENTRYPOINT ["./start.sh"]
