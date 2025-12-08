FROM python:3.10.2

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TZ=Europe/Istanbul

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]