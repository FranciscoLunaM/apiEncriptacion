FROM python:3.12.4-slim
WORKDIR .
COPY ./api ./
COPY requirements.txt ./

RUN pip3 install -r requirements.txt
