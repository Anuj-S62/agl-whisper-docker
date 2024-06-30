FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install -r requirements.txt

ENV MODEL_URL=https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt

RUN wget -P ./models ${MODEL_URL}

ENV CONFIG_PATH=/app/config.ini

EXPOSE 50051

CMD ["python", "agl_whisper_service.py", "run-server", "--default"]
