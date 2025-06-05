FROM python:3.12-slim

WORKDIR /app

RUN pip install flask requests

COPY server.py .

EXPOSE 5000

CMD ["python", "server.py"]

LABEL authors="floressek"