FROM python:3.11

ENV PYTHONUNBUFFERED 1

EXPOSE 8080
WORKDIR /api

COPY . /api
RUN pip install -r requirements.txt

CMD [ "uvicorn", "app.main:app", "--port", "8080", "--host", "0.0.0.0"]