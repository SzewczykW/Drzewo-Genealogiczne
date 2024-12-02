FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN python3 -m pip install -r requirements.txt

EXPOSE 80

CMD ["python3", "manage.py", "runserver", "0.0.0.0:80"]
