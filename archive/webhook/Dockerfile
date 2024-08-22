FROM python:buster

COPY . /app

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "simple_api.py"]
