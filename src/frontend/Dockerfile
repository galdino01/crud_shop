FROM python:3.7-alpine

RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app
CMD ["flask","run","--host=0.0.0.0"]