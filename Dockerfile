# syntax=docker/dockerfile:1.2
FROM python:3.9
# put you docker configuration here.

WORKDIR /code

COPY ./requirements* /code/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt -r /code/requirements-dev.txt -r /code/requirements-test.txt

COPY ./data /code/data
COPY ./model.pkl /code/model.pkl
COPY ./tests /code/tests
COPY ./challenge /code/challenge


# must be 0.0.0.0:8080 because of fly.io
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8080"]