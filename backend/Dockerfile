FROM python:3.11-slim

WORKDIR /app

RUN sed -i 's/deb.debian.org/mirrors.tencentyun.com/g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update && apt-get install -y openssh-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -i https://mirrors.tencentyun.com/pypi/simple -r requirements.txt

COPY . .

RUN mkdir -p /app/data /app/ssh_keys

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
