FROM python:3.12.4-slim
WORKDIR /apiEncriptacion
COPY . /apiEncriptacion

RUN pip install -r requirements.txt