FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY health-checker.py .

ENTRYPOINT ["python", "health-checker.py", "/config/config.yaml"]
