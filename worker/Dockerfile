FROM python:3.12-slim

WORKDIR /home/myapp

COPY ./requirements.txt /home/myapp

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "/home/myapp/cosumer.py"]
