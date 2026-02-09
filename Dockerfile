FROM python:3.11.14-alpine

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "main.py" ]
CMD [ "-h" ]