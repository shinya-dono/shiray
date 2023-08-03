FROM python:3.10

USER root
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y openssh-server lsof

WORKDIR /code

COPY . /code/

RUN pip install -r /code/requirements.txt
RUN chmod -R 777 /code

RUN mkdir /var/run/sshd
RUN echo 'root:screencast' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
#CMD ["/usr/sbin/sshd", "-D"]

#EXPOSE 80
#CMD ["python3","/code/main.py"]

#COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]