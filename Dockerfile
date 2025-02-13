# Use Python as the base image
FROM python:3.9-slim

# Set the environment variables
ENV PYTHONPATH=/app
ENV DISPLAY=:99

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    xvfb \
    libgl1-mesa-glx \
    libxkbcommon-x11-0 \
    libxcb-xinerama0

# Copy the application files
COPY src/ ./src/
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the necessary ports
EXPOSE 8080

# Command to run the application
CMD ["xvfb-run", "python", "./src/main.py"]
