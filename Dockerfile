FROM python:3.10

ENV PYTHONUNBUFFERED 1
WORKDIR /code

COPY src/requirements.txt /code/

RUN apt update && apt install vim curl -y

RUN pip install -r /code/requirements.txt

CMD ["python3","/code/main.py"]
