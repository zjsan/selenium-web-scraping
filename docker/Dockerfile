# Use a slim Python image to keep things fast and small
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY src/ ./src/

# Create the downloads directory inside the container
RUN mkdir /data

# Run the script
CMD ["python", "src/main.py"]