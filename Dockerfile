FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install -r requirements.txt

ENV CONFIG_PATH=/app/config.ini

EXPOSE 50051

CMD ["python", "agl_whisper_service.py", "run-server", "--default"]
