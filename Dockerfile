# Use an official, lightweight Python runtime
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies if required (clean up cache immediately)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to exploit Docker layer caching
COPY Requirements.txt .

# Install dependencies and download the spaCy model
RUN pip install --no-cache-dir -r Requirements.txt && \
    python -m spacy download en_core_web_sm

# Copy the rest of the application code
COPY app.py .

# Expose the standard Gradio port
EXPOSE 7860

# Set environment variables to keep Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "app.py"]
