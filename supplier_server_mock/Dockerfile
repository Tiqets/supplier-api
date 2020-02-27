FROM python:3.7-alpine

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app

RUN apk --update add python3-dev build-base linux-headers pcre-dev
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uwsgi", "app.ini"]
