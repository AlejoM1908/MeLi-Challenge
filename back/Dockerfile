FROM python:3.10.13-alpine3.18

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]