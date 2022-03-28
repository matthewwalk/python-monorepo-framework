# syntax=docker/dockerfile:1

FROM python:3.9 AS base
WORKDIR /app
RUN pip install -U pip 
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

FROM base AS build
CMD [ "python", "server.py"]