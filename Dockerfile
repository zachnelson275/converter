# Use official Python slim image
FROM python:3.10-slim

# Install system dependencies (potrace and image tools)
RUN apt-get update && \
    apt-get install -y potrace libglib2.0-0 libsm6 libxext6 libxrender-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Expose the port Flask will run on
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run", "--port=5000"]
