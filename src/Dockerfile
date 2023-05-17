FROM python:3.10

USER root
ENV PYTHONUNBUFFERED 1
WORKDIR /code

COPY . /code/

RUN pip install -r /code/requirements.txt
RUN chmod -R 777 /code

#EXPOSE 80
CMD ["python3","/code/main.py"]
