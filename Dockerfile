FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the application code
COPY ./app /app

# Expose the port
EXPOSE 8050

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "app.main:server"]