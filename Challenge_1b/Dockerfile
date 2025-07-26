FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Install system dependencies for PDF processing
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the processing script
COPY process_collections.py .

# Copy collections data
COPY Collection\ 1/ ./Collection\ 1/
COPY Collection\ 2/ ./Collection\ 2/  
COPY Collection\ 3/ ./Collection\ 3/

# Run the script
CMD ["python", "process_collections.py"]
