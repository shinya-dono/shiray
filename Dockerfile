FROM python:3.10

WORKDIR /code
COPY src/ /code

COPY /src/service/* /etc/systemd/system/

ADD * .
RUN pip install -r /code/requirements.txt

CMD ["systemctl", "restart", "xray.service"]
CMD ["systemctl", "restart", "shiray.service"]