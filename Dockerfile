# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY agent_prioritazion.py ./
COPY frontend.html ./

# Expose port
EXPOSE 8000

# Set environment variable for Python
ENV PYTHONUNBUFFERED=1

# Command to run the app
CMD ["uvicorn", "agent_prioritazion:app", "--host", "0.0.0.0", "--port", "8000"] 