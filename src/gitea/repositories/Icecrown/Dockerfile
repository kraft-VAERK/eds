FROM ubuntu:20.04

RUN apt update
RUN apt upgrade -y

# Install Python 3 and pip
RUN apt install python3 python3-pip -y

# Check Python version
RUN python3 --version

ENV server-app=server-app

RUN pip install playwright

RUN touch /etc/localtime

RUN echo "Europe/Rome" >> /etc/localtime

RUN playwright install

RUN playwright install-deps

CMD [ "echo", "running tests" ]