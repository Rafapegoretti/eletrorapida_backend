FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]