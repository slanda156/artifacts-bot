FROM python:3

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY ./main.py /app/main.py
COPY ./src /app/src
COPY ./logger.yaml /app/logger.yaml

CMD ["python", "/app/main.py"]