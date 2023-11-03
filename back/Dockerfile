FROM python:3.11.5-alpine3.18

WORKDIR /app

COPY . /app

RUN apk add --no-cache gcc musl-dev

RUN pip install --upgrade pip wheel setuptools
RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]