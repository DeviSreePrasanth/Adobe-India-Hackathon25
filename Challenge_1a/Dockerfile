FROM --platform=linux/amd64 python:3.10 as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


FROM --platform=linux/amd64 python:3.10.14-slim

RUN apt-get update && apt-get upgrade -y && apt-get clean

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

COPY process_pdfs.py .

CMD ["python", "process_pdfs.py"]