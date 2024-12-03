FROM python:3

# Copy requirements file and install dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copy application files
COPY main.py /app/main.py
COPY src /app/src
COPY logger.yaml /app/logger.yaml
COPY keys /app/keys

RUN chmod +x /app/main.py
RUN chmod -R +x /app/src/

# Set working directory (optional but good practice)
WORKDIR /app

# Command to run the application
CMD ["python", "main.py"]
