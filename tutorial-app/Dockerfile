# Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code (including app.py and init_db.py) into the container at /app
COPY . .

# Expose the port that the Flask app will run on
EXPOSE 5000

# Define environment variables for Flask (can be overridden by Kubernetes ConfigMap/Secret)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
# DATABASE_URL and FLASK_SECRET_KEY will be set by Kubernetes Deployment envFrom/env

# Command to run the Flask application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

