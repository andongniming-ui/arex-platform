FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y openssh-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copy pre-downloaded arex-agent.jar into the container
RUN mkdir -p /app/data /app/ssh_keys /opt/arex-agent
COPY arex-agent/arex-agent.jar /opt/arex-agent/arex-agent.jar

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
